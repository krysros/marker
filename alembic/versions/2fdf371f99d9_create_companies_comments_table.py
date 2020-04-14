"""create companies_comments table

Revision ID: 2fdf371f99d9
Revises: 830bd84561f9
Create Date: 2020-04-14 17:02:46.140923

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2fdf371f99d9'
down_revision = '830bd84561f9'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'companies_comments',
        sa.Column('company_id', sa.Integer, sa.ForeignKey('companies.id',
                                                          onupdate='CASCADE',
                                                          ondelete='CASCADE')),
        sa.Column('comment_id', sa.Integer, sa.ForeignKey('comments.id',
                                                          onupdate='CASCADE',
                                                          ondelete='CASCADE')),
    )


def downgrade():
    op.drop_table('companies_comments')
