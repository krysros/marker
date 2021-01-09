"""add columns to company table

Revision ID: a8b88ed658b6
Revises: e73943f774d7
Create Date: 2021-01-09 23:06:19.602064

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a8b88ed658b6'
down_revision = 'e73943f774d7'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('companies', sa.Column('street', sa.Unicode(100)))
    op.add_column('companies', sa.Column('postcode', sa.Unicode(10)))
    op.add_column('companies', sa.Column('court', sa.Unicode(100)))


def downgrade():
    op.drop_column('companies', 'street')
    op.drop_column('companies', 'postcode')
    op.drop_column('companies', 'court')
