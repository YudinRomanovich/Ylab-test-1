"""empty message

Revision ID: af78e35e6ddb
Revises: 7aafa387f4e6
Create Date: 2024-01-27 19:20:25.568157

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'af78e35e6ddb'
down_revision: Union[str, None] = '7aafa387f4e6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("menu", sa.Column('dishes_count', sa.Integer, default=0))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("menu", "dishes_count")
    # ### end Alembic commands ###