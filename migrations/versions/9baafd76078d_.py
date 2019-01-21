"""empty message

Revision ID: 9baafd76078d
Revises: 3a283ab36083
Create Date: 2019-01-12 19:12:33.719578

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9baafd76078d'
down_revision = '3a283ab36083'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('hits', sa.Column('ignore', sa.Boolean(), nullable=True))
    op.drop_column('hits', 'marked_for_deletion')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('hits', sa.Column('marked_for_deletion', sa.BOOLEAN(), autoincrement=False, nullable=True))
    op.drop_column('hits', 'ignore')
    # ### end Alembic commands ###
