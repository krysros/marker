"""add link column to investors table

Revision ID: 8aaa5b31e2a6
Revises: 73bfa6afc131
Create Date: 2020-07-27 22:11:57.449596

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8aaa5b31e2a6'
down_revision = '73bfa6afc131'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('investors', sa.Column('link', sa.Unicode(2000)))


def downgrade():
    op.drop_column('investors', 'link')
