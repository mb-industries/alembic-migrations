"""add explicit feedback fields to event_reviews

Revision ID: g4h5i6j7a8b
Revises: f3a4b5c6_add_event_review_events
Create Date: 2025-10-23 18:00:00
"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'g4h5i6j7a8b'
down_revision = 'f3a4b5c6_add_event_review_events'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('event_reviews', sa.Column('liked', sa.Text(), nullable=True))
    op.add_column('event_reviews', sa.Column('improve', sa.Text(), nullable=True))


def downgrade():
    try:
        op.drop_column('event_reviews', 'improve')
    except Exception:
        pass
    try:
        op.drop_column('event_reviews', 'liked')
    except Exception:
        pass
