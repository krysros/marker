"""add voivodeship column to investors table

Revision ID: 9ef5995237b7
Revises: 8aaa5b31e2a6
Create Date: 2020-07-27 23:45:43.646440

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9ef5995237b7'
down_revision = '8aaa5b31e2a6'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('investors', sa.Column('voivodeship', sa.Unicode(2)))


def downgrade():
    op.drop_column('investors', 'voivodeship')
