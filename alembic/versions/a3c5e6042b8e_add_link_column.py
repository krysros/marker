"""add link column

Revision ID: a3c5e6042b8e
Revises: 2fdf371f99d9
Create Date: 2020-04-17 11:56:14.907707

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a3c5e6042b8e'
down_revision = '2fdf371f99d9'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('tenders', sa.Column('link', sa.Unicode(2000)))


def downgrade():
    op.drop_column('tenders', 'link')
 