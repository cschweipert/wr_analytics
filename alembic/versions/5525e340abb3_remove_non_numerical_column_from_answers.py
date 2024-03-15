"""Remove non_numerical column from answers

Revision ID: 5525e340abb3
Revises: e940f3f363c9
Create Date: 2024-03-15 14:19:43.269791

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5525e340abb3'
down_revision: Union[str, None] = 'e940f3f363c9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Instructions to drop the 'non_numerical' column
    op.drop_column('answers', 'non_numerical')


def downgrade():
    # Instructions to add the 'non_numerical' column back if needed
    op.add_column('answers',
                  sa.Column('non_numerical', sa.String(), nullable=True))
