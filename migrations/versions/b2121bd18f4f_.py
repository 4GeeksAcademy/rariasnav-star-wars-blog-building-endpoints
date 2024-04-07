"""empty message

Revision ID: b2121bd18f4f
Revises: 14ba200e023e
Create Date: 2024-04-07 18:25:21.139770

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b2121bd18f4f'
down_revision = '14ba200e023e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('like',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('starship_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['starship_id'], ['starship.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('like')
    # ### end Alembic commands ###
