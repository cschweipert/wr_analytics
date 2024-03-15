"""Add flag column and remove comment column from answers

Revision ID: 69b24e6993f0
Revises: 69d3fc9ca797
Create Date: 2024-03-15 13:05:42.619553

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '69b24e6993f0'
down_revision: Union[str, None] = '69d3fc9ca797'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('answers',
                  sa.Column('flag', sa.Boolean(), nullable=True))
    op.drop_column('answers', 'comments')


def downgrade():
    op.add_column('answers',
                  sa.Column('comments', sa.String(), nullable=True))
    op.drop_column('answers', 'flag')
