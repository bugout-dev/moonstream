"""Labels for addresses

Revision ID: 4d69885b673a
Revises: 571f33ad7587
Create Date: 2021-08-09 12:18:54.670225

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '4d69885b673a'
down_revision = '571f33ad7587'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_ethereum_smart_contracts_address', table_name='ethereum_smart_contracts')
    op.drop_index('ix_ethereum_smart_contracts_transaction_hash', table_name='ethereum_smart_contracts')
    
    op.execute("ALTER TABLE ethereum_smart_contracts RENAME TO ethereum_addresses;")
    op.alter_column("ethereum_addresses", "transaction_hash", nullable=True)
    op.add_column('ethereum_addresses', sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text("TIMEZONE('utc', statement_timestamp())"), nullable=False))
    
    op.create_index(op.f('ix_ethereum_addresses_address'), 'ethereum_addresses', ['address'], unique=False)
    op.create_index(op.f('ix_ethereum_addresses_transaction_hash'), 'ethereum_addresses', ['transaction_hash'], unique=False)
    
    op.create_table('ethereum_labels',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('label', sa.VARCHAR(length=256), nullable=False),
    sa.Column('address', sa.Integer(), nullable=False),
    sa.Column('label_data', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text("TIMEZONE('utc', statement_timestamp())"), nullable=False),
    sa.ForeignKeyConstraint(['address'], ['ethereum_addresses.id'], name=op.f('fk_ethereum_labels_address_ethereum_addresses'), ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_ethereum_labels')),
    sa.UniqueConstraint('id', name=op.f('uq_ethereum_labels_id'))
    )
    op.create_index(op.f('ix_ethereum_labels_address'), 'ethereum_labels', ['address'], unique=False)
    op.create_index(op.f('ix_ethereum_labels_label'), 'ethereum_labels', ['label'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_ethereum_addresses_transaction_hash'), table_name='ethereum_addresses')
    op.drop_index(op.f('ix_ethereum_addresses_address'), table_name='ethereum_addresses')

    op.execute("ALTER TABLE ethereum_addresses RENAME TO ethereum_smart_contracts;")
    op.alter_column("ethereum_smart_contracts", "transaction_hash", nullable=False)
    op.drop_column('ethereum_smart_contracts', 'created_at')
    
    op.create_index('ix_ethereum_smart_contracts_transaction_hash', 'ethereum_smart_contracts', ['transaction_hash'], unique=False)
    op.create_index('ix_ethereum_smart_contracts_address', 'ethereum_smart_contracts', ['address'], unique=False)

    op.drop_index(op.f('ix_ethereum_labels_label'), table_name='ethereum_labels')
    op.drop_index(op.f('ix_ethereum_labels_address'), table_name='ethereum_labels')
    op.drop_table('ethereum_labels')
    # ### end Alembic commands ###