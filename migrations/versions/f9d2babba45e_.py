"""empty message

Revision ID: f9d2babba45e
Revises: 189681869d4d
Create Date: 2019-01-13 10:50:14.760572

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f9d2babba45e'
down_revision = '189681869d4d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('hits', sa.Column('interview', sa.Boolean(), nullable=True))
    op.drop_column('hits', 'interviewed')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('hits', sa.Column('interviewed', sa.BOOLEAN(), autoincrement=False, nullable=True))
    op.drop_column('hits', 'interview')
    # ### end Alembic commands ###
