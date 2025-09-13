"""add mock tests table

Revision ID: 2d608d398867
Revises: f22601e514ca
Create Date: 2025-09-10 00:00:00.000000
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '2d608d398867'
down_revision = 'f22601e514ca'
branch_labels = None
depends_on = None


def upgrade():
    status_enum = sa.Enum('pending', 'processing', 'ready', 'error', name='mock_test_status_enum')
    status_enum.create(op.get_bind(), checkfirst=True)
    op.create_table(
        'mock_tests',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('library_id', sa.Integer(), nullable=False),
        sa.Column('name', sa.Text(), nullable=False),
        sa.Column('material_ids', sa.JSON(), nullable=False),
        sa.Column('status', status_enum, nullable=False, server_default='pending'),
        sa.Column('questions', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['library_id'], ['library.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    op.drop_table('mock_tests')
    status_enum = sa.Enum(name='mock_test_status_enum')
    status_enum.drop(op.get_bind(), checkfirst=True)
