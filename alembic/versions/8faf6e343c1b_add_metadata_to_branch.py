"""add metadata to branch

Revision ID: 8faf6e343c1b
Revises: c6b00aa2a2c7
Create Date: 2020-04-17 19:53:41.949774

"""
import datetime
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8faf6e343c1b'
down_revision = 'c6b00aa2a2c7'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('branches',
                  sa.Column('added', sa.DateTime,
                            default=datetime.datetime.now))
    op.add_column('branches',
                  sa.Column('edited', sa.DateTime,
                            default=datetime.datetime.now,
                            onupdate=datetime.datetime.now))
    op.add_column('branches',
                  sa.Column('submitter_id', sa.Integer,
                            sa.ForeignKey('users.id', ondelete='SET NULL')))
    op.add_column('branches',
                  sa.Column('editor_id', sa.Integer,
                            sa.ForeignKey('users.id', ondelete='SET NULL')))


def downgrade():
    op.drop_column('branches', 'added')
    op.drop_column('branches', 'edited')
    op.drop_column('branches', 'submitter_id')
    op.drop_column('branches', 'editor_id')
