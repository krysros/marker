"""create marker table

Revision ID: a8204ddd4088
Revises: 
Create Date: 2018-04-29 11:55:03.273247

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a8204ddd4088'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'marker',
        sa.Column('company_id', sa.Integer,
           sa.ForeignKey('companies.id', onupdate='CASCADE', ondelete='CASCADE')),
        sa.Column('user_id', sa.Integer,
           sa.ForeignKey('users.id', onupdate='CASCADE', ondelete='CASCADE')),
    )


def downgrade():
     op.drop_table('marker')
