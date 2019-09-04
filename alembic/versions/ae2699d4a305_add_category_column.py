"""add category column

Revision ID: ae2699d4a305
Revises: a8204ddd4088
Create Date: 2019-09-04 16:49:37.320255

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ae2699d4a305'
down_revision = 'a8204ddd4088'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('companies', sa.Column('category', sa.Unicode(10), server_default='default'))


def downgrade():
    op.drop_column('companies', 'category')
