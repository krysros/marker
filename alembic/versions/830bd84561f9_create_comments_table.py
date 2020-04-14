"""create comments table

Revision ID: 830bd84561f9
Revises: ae2699d4a305
Create Date: 2020-04-13 14:17:53.819025

"""
import datetime
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '830bd84561f9'
down_revision = 'ae2699d4a305'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'comments',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('comment', sa.Text),
        sa.Column('added', sa.DateTime, default=datetime.datetime.now),
        sa.Column('submitter_id', sa.Integer, sa.ForeignKey('users.id', ondelete='SET NULL')),
    )


def downgrade():
    op.drop_table('comments')
