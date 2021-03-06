"""empty message

Revision ID: 6e28321a7d31
Revises: 7c08c7f24f68
Create Date: 2020-02-12 10:51:49.011312

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6e28321a7d31'
down_revision = '7c08c7f24f68'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('product_line',
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('name', sa.String(length=30), nullable=True),
    sa.Column('id_category', sa.String(length=36), nullable=True),
    sa.Column('profit_percent', sa.Float(precision=2), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
    sa.ForeignKeyConstraint(['id_category'], ['category.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('address', schema=None) as batch_op:
        batch_op.alter_column('provider_id',
               existing_type=sa.VARCHAR(length=36),
               nullable=False)
        batch_op.create_index(batch_op.f('ix_address_provider_id'), ['provider_id'], unique=False)
        batch_op.drop_constraint('address_provider_id_key', type_='unique')

    with op.batch_alter_table('category', schema=None) as batch_op:
        batch_op.add_column(sa.Column('profit_percent', sa.Float(precision=2), nullable=True))

    with op.batch_alter_table('products', schema=None) as batch_op:
        batch_op.add_column(sa.Column('created_at', sa.DateTime(timezone=True), nullable=True))
        batch_op.add_column(sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True))
        batch_op.add_column(sa.Column('id_product_line', sa.String(length=36), nullable=True))
        batch_op.add_column(sa.Column('measure_unit', sa.String(length=10), nullable=False))
        batch_op.add_column(sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True))
        batch_op.create_unique_constraint(None, ['name'])
        batch_op.create_foreign_key(None, 'product_line', ['id_product_line'], ['id'])
        batch_op.drop_column('product_line')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('products', schema=None) as batch_op:
        batch_op.add_column(sa.Column('product_line', sa.VARCHAR(length=36), autoincrement=False, nullable=True))
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='unique')
        batch_op.drop_column('updated_at')
        batch_op.drop_column('measure_unit')
        batch_op.drop_column('id_product_line')
        batch_op.drop_column('deleted_at')
        batch_op.drop_column('created_at')

    with op.batch_alter_table('category', schema=None) as batch_op:
        batch_op.drop_column('profit_percent')

    with op.batch_alter_table('address', schema=None) as batch_op:
        batch_op.create_unique_constraint('address_provider_id_key', ['provider_id'])
        batch_op.drop_index(batch_op.f('ix_address_provider_id'))
        batch_op.alter_column('provider_id',
               existing_type=sa.VARCHAR(length=36),
               nullable=True)

    op.drop_table('product_line')
    # ### end Alembic commands ###
