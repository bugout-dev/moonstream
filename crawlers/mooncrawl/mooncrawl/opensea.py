import argparse
import base64
from datetime import datetime, timedelta
import json
from pprint import pprint
import string
import time
from typing import Any, Collection, Dict

from moonstreamdb.models import EthereumAddress, EthereumLabel, OpenSeaCrawlingState
from moonstreamdb.db import yield_db_session_ctx
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import func
import requests

session = requests.Session()

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0",
}


def make_request(headers: Dict[str, Any], data: Dict[str, Any]):
    """
    Here just do request and return json response
    all graphql request return Too 'many requests'
    if we exceeded rate limit
    API looks similar like github but looks like have different limits
    for not just hardcoded timer
    """
    repeat = 0
    time.sleep(3)

    try:

        while True:
            try:
                graphql_resp = session.get(
                    "https://api.opensea.io/graphql/",
                    headers=headers,
                    json=data,
                )
            except Exception as err:
                print(f"Error on get request status {graphql_resp.status_code} ")
                repeat += 1
                time.sleep(10)
                if repeat >= 3:
                    break

            if "Too many requests" in graphql_resp.text:
                time.sleep(3)
            else:
                break

        # Too many requests. Please wait 180559 microseconds.
        json_response = graphql_resp.json()
    except Exception as err:
        print(err)
        print(graphql_resp.text)
        json_response = {}

    return json_response


def check_if_third_requred(query: str, data: Dict[str, Any]):

    """
    Check if request to 9900 cursor exist it meen we need to go deeper.png
    """

    required = False

    message = str(f"arrayconnection:{9899}")
    message_bytes = message.encode("ascii")
    base64_bytes = base64.b64encode(message_bytes)

    data["variables"]["cursor"] = base64_bytes.decode("utf-8")

    data["variables"]["query"] = query

    response_result = make_request(headers=headers, data=data)

    try:
        print(
            f'last coursor len {len(response_result["data"]["query"]["collections"]["edges"])}'
        )
        print(response_result["data"]["query"]["collections"]["edges"][0])
        required = True
    except TypeError:
        pass
    except IndexError:
        pass
    except Exception as err:
        print(err)
        raise
    return required


def write_contract_to_database(
    db_session: Session,
    token_address: str,
    blockchain: str,
    name: str,
    slug: str,
    image_url: str,
):
    """
    Write to datbase
    Check if address exists on database
    if not exists then get id and write label
    """

    address_id = (
        db_session.query(EthereumAddress.id)
        .filter(EthereumAddress.address == token_address)
        .one_or_none()
    )

    if not address_id:
        try:
            register_address = EthereumAddress(address=token_address)
            db_session.add(register_address)
            db_session.commit()
            address_id = register_address.id
        except Exception as err:

            db_session.rollback()
            print(f"Error adding address to database: {err}")
    else:
        address_id = address_id[0]

    label_data = {
        "name": name,
        "opensea_url": f"https://opensea.io/assets/{slug}",
        "blockchain": blockchain,
        "imageUrl": image_url,
    }

    eth_label = EthereumLabel(
        label="opensea_nft",
        address_id=address_id,
        label_data=label_data,
    )
    try:
        db_session.add(eth_label)
        db_session.commit()
    except Exception as err:
        print(f"Failed adding {name} label to db err: {err}")
        db_session.rollback()


def parse_contract(db_session: Session, collection: Dict[str, Any]):
    """
    Parse object wich come from graphql query
    """

    try:
        name = collection["node"]["name"]
        slug = collection["node"]["slug"]
        contract_address = collection["node"]["representativeAsset"]["assetContract"][
            "address"
        ]
        blockchain = collection["node"]["representativeAsset"]["assetContract"]["chain"]
        image_url = collection["node"]["imageUrl"]
        write_contract_to_database(
            db_session=db_session,
            token_address=contract_address,
            blockchain=blockchain,
            name=name,
            slug=slug,
            image_url=image_url,
        )
    except Exception as err:
        print(f"Can't read metadata from Graphql response: {err}")


def crawl_collections_query_loop(
    db_session: Session,
    query: str,
    payload: Dict[str, Any],
):

    """
    Main loop wich do requests based on cursor
    when it return incorrect response
    API rate limit handling on request method.
    """
    print(f"Start query='{query}'")

    already_parsed = (
        db_session.query(EthereumLabel.label_data["name"])
        .filter(func.lower(EthereumLabel.label_data["name"].astext).startswith(query))
        .all()
    )

    query_state = (
        db_session.query(OpenSeaCrawlingState)
        .filter(OpenSeaCrawlingState.query == query)
        .one_or_none()
    )

    # Try crawl new data from old position only for somethink which older 7 days
    if query_state is None:
        try:
            query_state = OpenSeaCrawlingState(query=query, total_count=0)
            db_session.add(query_state)
            db_session.commit()
            db_session.refresh(query_state)
        except Exception as err:
            db_session.rollback()
            print(f"Error add new {query} : {err}")
            return
        start_cursour = 0
    else:
        if query_state.updated_at.replace(tzinfo=None) > datetime.utcnow().replace(
            tzinfo=None
        ) - timedelta(days=7):
            return
        start_cursour = query_state.total_count

    total_write = 0  # just for logs

    array_of_collection = []

    while True:

        message = str(f"arrayconnection:{start_cursour}")
        message_bytes = message.encode("ascii")
        base64_bytes = base64.b64encode(message_bytes)

        payload["variables"]["cursor"] = base64_bytes.decode("utf-8")

        payload["variables"]["query"] = query

        json_response = make_request(headers=headers, data=payload)

        try:
            start_cursour += len(json_response["data"]["query"]["collections"]["edges"])
            json_response["data"]["query"]["collections"]["edges"][0]
        except TypeError:
            break
        except IndexError:
            break
        except Exception as err:
            raise

        array_of_collection = json_response["data"]["query"]["collections"]["edges"]

        for collection_types_oblect in array_of_collection:

            if (
                collection_types_oblect["node"]["representativeAsset"]
                and collection_types_oblect["node"]["name"] not in already_parsed
            ):
                parse_contract(
                    db_session=db_session, collection=collection_types_oblect
                )
                total_write += 1

    print(f"query: '{query}' write labels to database: {total_write} new labels")
    print(f"Last cursour position: {start_cursour + len(array_of_collection)}")
    try:
        query_state.total_count = start_cursour + len(array_of_collection)

        query_state.updated_at = datetime.now()
        db_session.commit()
    except Exception as err:
        db_session.rollback()
        print(f"Error update {query} : {err}")


def recurce_query_extend(
    db_session, search_query, grapql_collections_payload, symbols_string
):
    """ """
    # check need more?
    more_required = check_if_third_requred(search_query, grapql_collections_payload)

    if more_required:

        for addition_letter in symbols_string:

            new_search_query = search_query + addition_letter

            recurce_query_extend(
                db_session, new_search_query, grapql_collections_payload, symbols_string
            )
    else:
        crawl_collections_query_loop(
            db_session, search_query, grapql_collections_payload
        )


def crawl_opensea(args: argparse.Namespace):

    """
    Use one session for crawling TODO(Andrey) Add headers and maybe ssl randomization
    """

    BASE_TOKEN_URL = "https://opensea.io/assets"

    page = session.get(BASE_TOKEN_URL, headers=headers)
    print(f"Initial request responce {page.status_code}")

    with yield_db_session_ctx() as db_session:
        grapql_collections_payload = {
            "id": "CollectionFilterQuery",
            "query": "query CollectionFilterQuery(\n  $assetOwner: IdentityInputType\n  $categories: [CollectionSlug!]\n  $chains: [ChainScalar!]\n  $collections: [CollectionSlug!]\n  $count: Int\n  $cursor: String\n  $includeHidden: Boolean\n  $query: String\n  $sortAscending: Boolean\n  $sortBy: CollectionSort\n) {\n  query {\n    ...CollectionFilter_data_421KmG\n  }\n}\n\nfragment CollectionFilter_data_421KmG on Query {\n  selectedCollections: collections(first: 25, collections: $collections, includeHidden: true) {\n    edges {\n      node {\n   stats {\n totalSupply\n }\n      TotalCount\n   representativeAsset {\n      assetContract {\n  name\n label\n  address\n     openseaVersion\n        id\n      }\n      id\n    }\n     imageUrl\n        name\n        slug\n        id\n      }\n    }\n  }\n  collections(after: $cursor, assetOwner: $assetOwner, chains: $chains, first: $count, includeHidden: $includeHidden, parents: $categories, query: $query, sortAscending: $sortAscending, sortBy: $sortBy) {\n    edges {\n      node {\n  author {\n address\n  id\n  }\n   TotalCount\n   representativeAsset {\n      assetContract {\n   address\n  chain\n   openseaVersion\n        id\n      }\n      id\n    }\n   assetCount\n  stats {\n totalSupply\n }\n      imageUrl\n        name\n        slug\n        id\n        __typename\n      }\n      cursor\n    }\n    pageInfo {\n      endCursor\n      hasNextPage\n  totalCount\n   }\n  }\n}\n",
            "variables": {
                "assetOwner": None,
                "categories": None,
                "chains": None,
                "collections": [],
                "count": 100,
                "cursor": "YXJyYXljb25uZWN0aW9uOjA=",
                "includeHidden": False,
                "query": None,
                "sortAscending": True,
                "sortBy": "CREATED_DATE",
            },
        }
        symbols_string = string.ascii_lowercase + "0123456789"

        for symbol in symbols_string:

            search_query = symbol

            recurce_query_extend(
                db_session,
                search_query,
                grapql_collections_payload,
                symbols_string,
            )


def main():
    """
    Crawl cli maybe need add one cli for all crawlers
    """

    parser = argparse.ArgumentParser(
        description="Crawls smart contract sources from etherscan.io"
    )
    parser.set_defaults(func=lambda _: parser.print_help())
    subcommands = parser.add_subparsers(description="Crawlers commands")

    crawl_parser = subcommands.add_parser(
        "crawl", description="Crawling data from source"
    )
    crawl_parser.set_defaults(func=lambda _: crawl_parser.print_help())
    subcommnds_crawl = crawl_parser.add_subparsers(
        description="Crawl rcontracts commands"
    )

    nft_parser = subcommnds_crawl.add_parser("nfts", description="Get nfts contracts")
    nft_parser.set_defaults(func=lambda _: nft_parser.print_help())
    nft_parser.set_defaults(func=crawl_opensea)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
