"""merge heads d0e1f2a3 and e2f3a4b5_add_event_reviews

Revision ID: f1a2b3c4_merge_heads
Revises: d0e1f2a3, e2f3a4b5_add_event_reviews
Create Date: 2025-10-22 21:45:00
"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'f1a2b3c4_merge_heads'
down_revision = ('d0e1f2a3', 'e2f3a4b5_add_event_reviews')
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass

