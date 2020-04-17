"""add city column

Revision ID: c6b00aa2a2c7
Revises: a3c5e6042b8e
Create Date: 2020-04-17 19:09:53.730723

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c6b00aa2a2c7'
down_revision = 'a3c5e6042b8e'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('investors', sa.Column('city', sa.Unicode(100)))


def downgrade():
    op.drop_column('investors', 'city')
 