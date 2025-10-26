"""optimize models: add cstone mapping + id_* indexes + pg_trgm

Revision ID: 7e9b6e6b8a1b_optimize_models
Revises: a026677ec9ad
Create Date: 2025-10-16 00:00:00
"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "7e9b6e6b8a1b_optimize_models"
down_revision = "05c61a1cfc1a"
branch_labels = None
depends_on = None


def _is_postgres(conn):
    return conn.dialect.name == "postgresql"


def upgrade():
    conn = op.get_bind()

    # Ensure pg_trgm exists on Postgres
    if _is_postgres(conn):
        op.execute("CREATE EXTENSION IF NOT EXISTS pg_trgm;")

    # Create mapping tables
    op.create_table(
        "cstone_item_map",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("cstone_item_id", sa.Integer(), nullable=False),
        sa.Column("item_id", sa.Integer(), nullable=True),
        sa.Column("match_confidence", sa.Float(), nullable=True),
        sa.Column("matched_at", sa.TIMESTAMP(), nullable=True),
        sa.UniqueConstraint("cstone_item_id", name="uq_cstone_item_map_item"),
    )

    op.create_table(
        "cstone_vehicle_map",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("cstone_vehicle_id", sa.Integer(), nullable=False),
        sa.Column("vehicle_id", sa.Integer(), nullable=True),
        sa.Column("match_confidence", sa.Float(), nullable=True),
        sa.Column("matched_at", sa.TIMESTAMP(), nullable=True),
        sa.UniqueConstraint("cstone_vehicle_id", name="uq_cstone_vehicle_map_vehicle"),
    )

    # Create simple btree indexes for all id_* columns across tables
    inspector = sa.inspect(conn)
    existing_indexes = {}
    for t in inspector.get_table_names():
        existing_indexes[t] = {ix['name'] for ix in inspector.get_indexes(t)}

    for table_name in inspector.get_table_names():
        cols = inspector.get_columns(table_name)
        for col in cols:
            name = col.get('name')
            if name and name.startswith('id_'):
                ix_name = f"ix_{table_name}_{name}"
                if ix_name not in existing_indexes.get(table_name, set()):
                    if _is_postgres(conn):
                        op.execute(sa.text(f'CREATE INDEX IF NOT EXISTS "{ix_name}" ON "{table_name}" ("{name}")'))
                    else:
                        # SQLite lacks IF NOT EXISTS for CREATE INDEX in older versions; try/catch
                        try:
                            op.execute(sa.text(f'CREATE INDEX "{ix_name}" ON "{table_name}" ("{name}")'))
                        except Exception:
                            pass


def downgrade():
    # Drop mapping tables
    op.drop_table("cstone_vehicle_map")
    op.drop_table("cstone_item_map")
    # Indexes left in place; safe to keep across downgrades.
