# """Add non_numerical column to answers

# Revision ID: e940f3f363c9
# Revises: a84e13bca48f
# Create Date: 2024-03-15 13:49:35.463950

# """
# from typing import Sequence, Union

# from alembic import op
# import sqlalchemy as sa


# # revision identifiers, used by Alembic.
# revision: str = 'e940f3f363c9'
# down_revision: Union[str, None] = 'a84e13bca48f'
# branch_labels: Union[str, Sequence[str], None] = None
# depends_on: Union[str, Sequence[str], None] = None


# def upgrade():
#     op.add_column('answers',
#                   sa.Column('non_numerical', sa.String(), nullable=True))


# def downgrade():
#     op.drop_column('answers', 'non_numerical')



from alembic import op
import sqlalchemy as sa

revision = 'e940f3f363c9'
down_revision = 'a84e13bca48f'
branch_labels = None
depends_on = None

def upgrade():
    # Attempt to drop the 'non_numerical' column if it already exists
    # Note: This operation may fail if the column does not exist.
    # You might need to manually handle such cases depending on your database.
    op.execute('ALTER TABLE answers DROP COLUMN IF EXISTS non_numerical CASCADE')
    
    # Recreate the 'non_numerical' column
    op.add_column('answers', sa.Column('non_numerical', sa.String(), nullable=True))

def downgrade():
    # Drop the 'non_numerical' column during downgrade
    op.drop_column('answers', 'non_numerical')

