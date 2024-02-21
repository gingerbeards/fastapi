"""add content column to posts table

Revision ID: c56271d7e6b7
Revises: 952fa5a9ea38
Create Date: 2024-02-20 23:03:40.723447

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c56271d7e6b7'
down_revision: Union[str, None] = '952fa5a9ea38'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', "content")
    pass
