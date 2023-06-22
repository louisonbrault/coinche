"""Add facebook id

Revision ID: ecec1f873edc
Revises: 68ff914fa880
Create Date: 2023-06-08 13:57:17.618312

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ecec1f873edc'
down_revision = '68ff914fa880'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('games', 'player_a2_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('games', 'player_b1_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('games', 'player_b2_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.add_column('users', sa.Column('facebook_id', sa.String(), nullable=True))
    op.create_unique_constraint(None, 'users', ['facebook_id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'users', type_='unique')
    op.drop_column('users', 'facebook_id')
    op.alter_column('games', 'player_b2_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('games', 'player_b1_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('games', 'player_a2_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###
