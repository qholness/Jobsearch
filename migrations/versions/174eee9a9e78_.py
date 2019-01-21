"""empty message

Revision ID: 174eee9a9e78
Revises: c042a1f6d78f
Create Date: 2019-01-19 02:00:29.500271

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '174eee9a9e78'
down_revision = 'c042a1f6d78f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('hits', 'summary')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('hits', sa.Column('summary', sa.VARCHAR(length=500), autoincrement=False, nullable=True))
    # ### end Alembic commands ###