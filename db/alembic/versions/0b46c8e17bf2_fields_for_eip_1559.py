"""fields-for-eip-1559

Revision ID: 0b46c8e17bf2
Revises: 240476c67b9f
Create Date: 2021-10-26 09:52:17.367528

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '0b46c8e17bf2'
down_revision = '240476c67b9f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('ethereum_blocks', sa.Column('base_fee_per_gas', sa.Numeric(precision=78, scale=0), nullable=True))
    op.add_column('ethereum_transactions', sa.Column('max_fee_per_gas', sa.Numeric(precision=78, scale=0), nullable=True))
    op.add_column('ethereum_transactions', sa.Column('max_priority_fee_per_gas', sa.Numeric(precision=78, scale=0), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('ethereum_transactions', 'max_priority_fee_per_gas')
    op.drop_column('ethereum_transactions', 'max_fee_per_gas')
    op.drop_column('ethereum_blocks', 'base_fee_per_gas')
    # ### end Alembic commands ###