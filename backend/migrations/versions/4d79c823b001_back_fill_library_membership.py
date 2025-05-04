"""back‑fill library_membership

Revision ID: 4d79c823b001
Revises: 1e63449266e0
Create Date: 2025-05-04 12:41:44.188827

"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, column
from datetime import datetime, timezone

# revision identifiers, used by Alembic.
revision = '4d79c823b001'
down_revision = '1e63449266e0'
branch_labels = None
depends_on = None

now = datetime.now(timezone.utc)

# For bulk_insert we'll declare a lightweight table object
library_membership = table(
    'library_membership',
    column('user_id', sa.Integer),
    column('library_id', sa.Integer),
    column('joined_at', sa.DateTime)
)

def upgrade():
    bind = op.get_bind()

    # 1️⃣  fetch all existing libraries & owners
    rows = bind.execute(sa.text("""
        SELECT id AS library_id, owner_id AS user_id
        FROM library
        WHERE owner_id IS NOT NULL
    """)).mappings().all()

    # 2️⃣  prepare bulk insert payload
    to_insert = [
        {"user_id": r["user_id"],
         "library_id": r["library_id"],
         "joined_at": now
         }         # optional column
        for r in rows
    ]

    # 3️⃣  insert, skipping duplicates if you re‑run
    if to_insert:
        op.bulk_insert(library_membership, to_insert)

def downgrade():
    bind = op.get_bind()
    bind.execute(sa.text("""
        DELETE FROM library_membership
        WHERE role = 'owner'
    """))
