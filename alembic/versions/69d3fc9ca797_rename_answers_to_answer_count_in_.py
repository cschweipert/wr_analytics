"""Rename answers to answer_count in metrics

Revision ID: 69d3fc9ca797
Revises: 998f56365035
Create Date: 2024-03-13 14:04:20.366596

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '69d3fc9ca797'
down_revision: Union[str, None] = '998f56365035'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.alter_column('metrics', 'answers', new_column_name='answer_count',
                    existing_type=sa.Integer())
    op.alter_column('raw_metrics', 'answers', new_column_name='answer_count',
                    existing_type=sa.Integer())


def downgrade():
    op.alter_column('metrics', 'answer_count', new_column_name='answers',
                    existing_type=sa.Integer())
    op.alter_column('raw_metrics', 'answer_count', new_column_name='answers',
                    existing_type=sa.Integer())
