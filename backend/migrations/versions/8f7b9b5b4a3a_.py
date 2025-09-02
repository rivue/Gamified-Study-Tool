"""empty message

Revision ID: 8f7b9b5b4a3a
Revises: eab43a8e62c0
Create Date: 2025-09-02 15:20:14.378733

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8f7b9b5b4a3a'
down_revision = 'eab43a8e62c0'
branch_labels = None
depends_on = None


def upgrade():
    op.execute("ALTER TYPE material_status_enum ADD VALUE IF NOT EXISTS 'pending'")


def downgrade():
    pass