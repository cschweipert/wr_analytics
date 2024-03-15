"""Add non_numerical column to answers

Revision ID: f9a230f774f3
Revises: 5525e340abb3
Create Date: 2024-03-15 14:22:46.683008

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f9a230f774f3'
down_revision: Union[str, None] = '5525e340abb3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('answers', sa.Column('non_numerical', sa.String()))


def downgrade() -> None:
    op.drop_column('answers', 'non_numerical')
