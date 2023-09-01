"""add apartment number col

Revision ID: 51a91daf4f04
Revises: d5d33024bc6b
Create Date: 2023-09-01 04:16:48.620165

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '51a91daf4f04'
down_revision: Union[str, None] = 'd5d33024bc6b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('address', sa.Column('apartment_number', sa.Integer(), nullable=True))


def downgrade() -> None:
    op.drop_column('address', 'apartment_number')
