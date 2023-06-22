"""Add display name column

Revision ID: 061d3a1a1328
Revises: 7e5f95044242
Create Date: 2023-06-07 15:16:20.783840

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '061d3a1a1328'
down_revision = '7e5f95044242'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('display_name', sa.String()))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'display_name')
    # ### end Alembic commands ###
