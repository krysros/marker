"""add price

Revision ID: 73bfa6afc131
Revises: 8faf6e343c1b
Create Date: 2020-04-19 10:26:02.631675

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '73bfa6afc131'
down_revision = '8faf6e343c1b'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('offers', sa.Column('category', sa.Unicode(20)))
    op.add_column('offers', sa.Column('unit', sa.Unicode(10)))
    op.add_column('offers', sa.Column('cost', sa.Numeric(precision=10, scale=2)))
    op.add_column('offers', sa.Column('currency', sa.Unicode(3)))


def downgrade():
    op.drop_column('offers', 'category')
    op.drop_column('offers', 'unit')
    op.drop_column('offers', 'cost')
    op.drop_column('offers', 'currency')
