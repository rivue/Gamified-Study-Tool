"""empty message

Revision ID: 7e48e816f729
Revises: bfc64c349606
Create Date: 2025-05-19 13:27:05.451626

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7e48e816f729'
down_revision = 'bfc64c349606'
branch_labels = None
depends_on = None


def upgrade():
# 1) add the nullable column first
    with op.batch_alter_table('library_section') as batch_op:
        batch_op.add_column(sa.Column('position', sa.Integer(), nullable=True))

    # 2) back-fill existing rows (one-based window fn works in Postgres;
    #    fallback to Python loop for SQLite)
    conn = op.get_bind()
    dialect = conn.dialect.name

    # PostgreSQL / SQLite ≥3.25 can use a window function
    if dialect == "sqlite":
        # one SELECT per row, but fine for dev DB sizes
        conn.execute(sa.text("""
            UPDATE library_section
            SET position = (
            SELECT COUNT(*)         -- zero-based rank
            FROM   library_section AS lu2
            WHERE  lu2.unit_id = library_section.unit_id
            AND    lu2.id < library_section.id
            )
        """))
    else:
        conn.execute(sa.text("""
            WITH ranked AS (
            SELECT id,
                    ROW_NUMBER() OVER
                    (PARTITION BY unit_id ORDER BY id) - 1 AS rn
            FROM   library_section
            )
            UPDATE library_section
            SET    position = ranked.rn
            FROM   ranked
            WHERE  ranked.id = library_section.id
        """))

    # 3) make the column NOT NULL and add the unique constraint
    with op.batch_alter_table('library_section') as batch_op:
        batch_op.alter_column('position', nullable=False)
        batch_op.create_unique_constraint('uq_unit_section_position',
                                          ['unit_id', 'position'])


def downgrade():
    with op.batch_alter_table('library_unit') as batch_op:
        batch_op.drop_constraint('uq_library_unit_position', type_='unique')
        batch_op.drop_column('position')
