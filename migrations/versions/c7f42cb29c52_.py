"""empty message

Revision ID: c7f42cb29c52
Revises: 635b69eb7b9b
Create Date: 2018-12-25 18:14:54.579520

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c7f42cb29c52'
down_revision = '635b69eb7b9b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('hits', 'company')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('hits', sa.Column('company', sa.INTEGER(), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
