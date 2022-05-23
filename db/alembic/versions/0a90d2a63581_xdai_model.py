"""xdai model

Revision ID: 0a90d2a63581
Revises: 5f5b8f19570f
Create Date: 2022-05-23 12:14:03.426937

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '0a90d2a63581'
down_revision = '5f5b8f19570f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('xdai_blocks',
    sa.Column('block_number', sa.BigInteger(), nullable=False),
    sa.Column('difficulty', sa.BigInteger(), nullable=True),
    sa.Column('extra_data', sa.VARCHAR(length=128), nullable=True),
    sa.Column('gas_limit', sa.BigInteger(), nullable=True),
    sa.Column('gas_used', sa.BigInteger(), nullable=True),
    sa.Column('base_fee_per_gas', sa.Numeric(precision=78, scale=0), nullable=True),
    sa.Column('hash', sa.VARCHAR(length=256), nullable=True),
    sa.Column('logs_bloom', sa.VARCHAR(length=1024), nullable=True),
    sa.Column('miner', sa.VARCHAR(length=256), nullable=True),
    sa.Column('nonce', sa.VARCHAR(length=256), nullable=True),
    sa.Column('parent_hash', sa.VARCHAR(length=256), nullable=True),
    sa.Column('receipt_root', sa.VARCHAR(length=256), nullable=True),
    sa.Column('uncles', sa.VARCHAR(length=256), nullable=True),
    sa.Column('size', sa.Integer(), nullable=True),
    sa.Column('state_root', sa.VARCHAR(length=256), nullable=True),
    sa.Column('timestamp', sa.BigInteger(), nullable=True),
    sa.Column('total_difficulty', sa.VARCHAR(length=256), nullable=True),
    sa.Column('transactions_root', sa.VARCHAR(length=256), nullable=True),
    sa.Column('indexed_at', sa.DateTime(timezone=True), server_default=sa.text("TIMEZONE('utc', statement_timestamp())"), nullable=False),
    sa.PrimaryKeyConstraint('block_number', name=op.f('pk_xdai_blocks'))
    )
    op.create_index(op.f('ix_xdai_blocks_block_number'), 'xdai_blocks', ['block_number'], unique=True)
    op.create_index(op.f('ix_xdai_blocks_hash'), 'xdai_blocks', ['hash'], unique=False)
    op.create_index(op.f('ix_xdai_blocks_timestamp'), 'xdai_blocks', ['timestamp'], unique=False)
    op.create_table('xdai_labels',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('label', sa.VARCHAR(length=256), nullable=False),
    sa.Column('block_number', sa.BigInteger(), nullable=True),
    sa.Column('address', sa.VARCHAR(length=256), nullable=True),
    sa.Column('transaction_hash', sa.VARCHAR(length=256), nullable=True),
    sa.Column('label_data', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    sa.Column('block_timestamp', sa.BigInteger(), nullable=True),
    sa.Column('log_index', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text("TIMEZONE('utc', statement_timestamp())"), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_xdai_labels')),
    sa.UniqueConstraint('id', name=op.f('uq_xdai_labels_id'))
    )
    op.create_index(op.f('ix_xdai_labels_address'), 'xdai_labels', ['address'], unique=False)
    op.create_index(op.f('ix_xdai_labels_block_number'), 'xdai_labels', ['block_number'], unique=False)
    op.create_index(op.f('ix_xdai_labels_block_timestamp'), 'xdai_labels', ['block_timestamp'], unique=False)
    op.create_index(op.f('ix_xdai_labels_label'), 'xdai_labels', ['label'], unique=False)
    op.create_index(op.f('ix_xdai_labels_transaction_hash'), 'xdai_labels', ['transaction_hash'], unique=False)
    op.create_table('xdai_transactions',
    sa.Column('hash', sa.VARCHAR(length=256), nullable=False),
    sa.Column('block_number', sa.BigInteger(), nullable=False),
    sa.Column('from_address', sa.VARCHAR(length=256), nullable=True),
    sa.Column('to_address', sa.VARCHAR(length=256), nullable=True),
    sa.Column('gas', sa.Numeric(precision=78, scale=0), nullable=True),
    sa.Column('gas_price', sa.Numeric(precision=78, scale=0), nullable=True),
    sa.Column('max_fee_per_gas', sa.Numeric(precision=78, scale=0), nullable=True),
    sa.Column('max_priority_fee_per_gas', sa.Numeric(precision=78, scale=0), nullable=True),
    sa.Column('input', sa.Text(), nullable=True),
    sa.Column('nonce', sa.VARCHAR(length=256), nullable=True),
    sa.Column('transaction_index', sa.BigInteger(), nullable=True),
    sa.Column('transaction_type', sa.Integer(), nullable=True),
    sa.Column('value', sa.Numeric(precision=78, scale=0), nullable=True),
    sa.Column('indexed_at', sa.DateTime(timezone=True), server_default=sa.text("TIMEZONE('utc', statement_timestamp())"), nullable=False),
    sa.ForeignKeyConstraint(['block_number'], ['xdai_blocks.block_number'], name=op.f('fk_xdai_transactions_block_number_xdai_blocks'), ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('hash', name=op.f('pk_xdai_transactions'))
    )
    op.create_index(op.f('ix_xdai_transactions_block_number'), 'xdai_transactions', ['block_number'], unique=False)
    op.create_index(op.f('ix_xdai_transactions_from_address'), 'xdai_transactions', ['from_address'], unique=False)
    op.create_index(op.f('ix_xdai_transactions_gas'), 'xdai_transactions', ['gas'], unique=False)
    op.create_index(op.f('ix_xdai_transactions_gas_price'), 'xdai_transactions', ['gas_price'], unique=False)
    op.create_index(op.f('ix_xdai_transactions_hash'), 'xdai_transactions', ['hash'], unique=True)
    op.create_index(op.f('ix_xdai_transactions_to_address'), 'xdai_transactions', ['to_address'], unique=False)
    op.create_index(op.f('ix_xdai_transactions_value'), 'xdai_transactions', ['value'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_xdai_transactions_value'), table_name='xdai_transactions')
    op.drop_index(op.f('ix_xdai_transactions_to_address'), table_name='xdai_transactions')
    op.drop_index(op.f('ix_xdai_transactions_hash'), table_name='xdai_transactions')
    op.drop_index(op.f('ix_xdai_transactions_gas_price'), table_name='xdai_transactions')
    op.drop_index(op.f('ix_xdai_transactions_gas'), table_name='xdai_transactions')
    op.drop_index(op.f('ix_xdai_transactions_from_address'), table_name='xdai_transactions')
    op.drop_index(op.f('ix_xdai_transactions_block_number'), table_name='xdai_transactions')
    op.drop_table('xdai_transactions')
    op.drop_index(op.f('ix_xdai_labels_transaction_hash'), table_name='xdai_labels')
    op.drop_index(op.f('ix_xdai_labels_label'), table_name='xdai_labels')
    op.drop_index(op.f('ix_xdai_labels_block_timestamp'), table_name='xdai_labels')
    op.drop_index(op.f('ix_xdai_labels_block_number'), table_name='xdai_labels')
    op.drop_index(op.f('ix_xdai_labels_address'), table_name='xdai_labels')
    op.drop_table('xdai_labels')
    op.drop_index(op.f('ix_xdai_blocks_timestamp'), table_name='xdai_blocks')
    op.drop_index(op.f('ix_xdai_blocks_hash'), table_name='xdai_blocks')
    op.drop_index(op.f('ix_xdai_blocks_block_number'), table_name='xdai_blocks')
    op.drop_table('xdai_blocks')
    # ### end Alembic commands ###
