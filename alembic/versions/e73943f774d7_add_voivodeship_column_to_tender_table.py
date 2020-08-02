"""add voivodeship column to tender table

Revision ID: e73943f774d7
Revises: 9ef5995237b7
Create Date: 2020-08-02 15:02:36.732433

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e73943f774d7'
down_revision = '9ef5995237b7'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('tenders', sa.Column('voivodeship', sa.Unicode(2)))


def downgrade():
    op.drop_column('tenders', 'voivodeship')
