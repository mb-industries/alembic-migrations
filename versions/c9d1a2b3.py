"""change suggestions.status to TEXT

Revision ID: c9d1a2b3
Revises: b1e2c3d4_update_sqlite_models
Create Date: 2025-10-16 16:11:23
"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "c9d1a2b3"
down_revision = "b1e2c3d4_update_sqlite_models"
branch_labels = None
depends_on = None

def upgrade():
    op.execute('ALTER TABLE suggestions ALTER COLUMN "status" TYPE TEXT USING "status"::text')

def downgrade():
    op.execute('ALTER TABLE suggestions ALTER COLUMN "status" TYPE INTEGER USING NULLIF("status", \'\')::integer')
