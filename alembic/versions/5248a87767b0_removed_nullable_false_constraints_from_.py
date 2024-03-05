"""Removed nullable=False constraints from answer columns

Revision ID: 5248a87767b0
Revises: 
Create Date: 2024-03-07 14:31:18.906322

"""
from alembic import op
import sqlalchemy as sa


revision = '5248a87767b0'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    with op.batch_alter_table('answers', schema=None) as batch_op:
        batch_op.alter_column('metric',
               existing_type=sa.String(),
               nullable=True)
        batch_op.alter_column('company',
               existing_type=sa.String(),
               nullable=True)
        batch_op.alter_column('value',
               existing_type=sa.String(),
               nullable=True)
        batch_op.alter_column('year',
               existing_type=sa.Integer(),
               nullable=True)
        batch_op.alter_column('url',
               existing_type=sa.String(),
               nullable=True)

def downgrade():
    with op.batch_alter_table('answers', schema=None) as batch_op:
        batch_op.alter_column('metric',
               existing_type=sa.String(),
               nullable=False)
        batch_op.alter_column('company',
               existing_type=sa.String(),
               nullable=False)
        batch_op.alter_column('value',
               existing_type=sa.String(),
               nullable=False)
        batch_op.alter_column('year',
               existing_type=sa.Integer(),
               nullable=False)
        batch_op.alter_column('url',
               existing_type=sa.String(),
               nullable=False)
