"""Add designers table and designer_id to answers

Revision ID: a84e13bca48f
Revises: 69b24e6993f0
Create Date: 2024-03-15 13:25:54.931423

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a84e13bca48f'
down_revision: Union[str, None] = '69b24e6993f0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table('designers',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(255), nullable=False)
    )

    op.add_column('answers',
        sa.Column('designer_id', sa.Integer, sa.ForeignKey('designers.id'), nullable=True)
    )


def downgrade():
    op.drop_column('answers', 'designer_id')
    op.drop_table('designers')
