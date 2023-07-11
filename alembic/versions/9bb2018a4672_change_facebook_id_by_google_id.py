"""Change facebook_id by google id

Revision ID: 9bb2018a4672
Revises: 0dad734de9d5
Create Date: 2023-06-30 11:33:18.229831

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9bb2018a4672'
down_revision = '0dad734de9d5'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('google_id', sa.String(), nullable=True))
    op.drop_constraint('users_facebook_id_key', 'users', type_='unique')
    op.create_unique_constraint(None, 'users', ['google_id'])
    op.drop_column('users', 'facebook_id')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('facebook_id', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'users', type_='unique')
    op.create_unique_constraint('users_facebook_id_key', 'users', ['facebook_id'])
    op.drop_column('users', 'google_id')
    # ### end Alembic commands ###