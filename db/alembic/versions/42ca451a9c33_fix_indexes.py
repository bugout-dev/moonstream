"""fix indexes

Revision ID: 42ca451a9c33
Revises: 2fa541f6f6fc
Create Date: 2022-06-07 13:30:40.746341

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "42ca451a9c33"
down_revision = "2fa541f6f6fc"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(
        "ix_polygon_labels_address_label_label_data_type_and_name",
        table_name="polygon_labels",
    )
    op.create_index(
        "ix_polygon_labels_address_block_number",
        "polygon_labels",
        ["address", "block_number"],
        unique=False,
    )
    op.create_index(
        "ix_polygon_labels_address_block_timestamp",
        "polygon_labels",
        ["address", "block_timestamp"],
        unique=False,
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute(
        """
        CREATE INDEX ix_polygon_labels_address_label_label_data_type_and_name ON polygon_labels USING BTREE (address,label,(label_data->>'type'),(label_data->>'name'));
        """
    )
    op.drop_index(
        "ix_polygon_labels_address_block_timestamp", table_name="polygon_labels"
    )
    op.drop_index("ix_polygon_labels_address_block_number", table_name="polygon_labels")
    # ### end Alembic commands ###
