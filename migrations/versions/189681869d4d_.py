"""empty message

Revision ID: 189681869d4d
Revises: 2d4dfcdbaedf
Create Date: 2019-01-13 10:47:10.506938

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '189681869d4d'
down_revision = '2d4dfcdbaedf'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('hits', sa.Column('interviewed', sa.Boolean(), nullable=True))
    op.add_column('hits', sa.Column('offered', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('hits', 'offered')
    op.drop_column('hits', 'interviewed')
    # ### end Alembic commands ###
