"""add event_reviews table for event feedback

Revision ID: e2f3a4b5_add_event_reviews
Revises: c9d1a2b3
Create Date: 2025-10-22 00:00:00
"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "e2f3a4b5_add_event_reviews"
down_revision = "c9d1a2b3"
branch_labels = None
depends_on = None


def upgrade():
    # Create table if not exists (Alembic will guard duplicates across DBs)
    op.create_table(
        'event_reviews',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('eventID', sa.BigInteger, nullable=False),
        sa.Column('userID', sa.BigInteger, nullable=False),
        sa.Column('rating', sa.Integer, nullable=True),
        sa.Column('review', sa.Text, nullable=True),
        sa.Column('created_at', sa.BigInteger, nullable=False, server_default='0'),
        sa.Column('updated_at', sa.BigInteger, nullable=False, server_default='0'),
    )
    op.create_index('ix_event_reviews_eventID', 'event_reviews', ['eventID'])
    op.create_index('ix_event_reviews_userID', 'event_reviews', ['userID'])
    # Emulate a unique constraint on (eventID, userID)
    try:
        op.create_unique_constraint('ux_event_reviews_event_user', 'event_reviews', ['eventID', 'userID'])
    except Exception:
        # Some SQLite versions may already have this; ignore
        pass


def downgrade():
    try:
        op.drop_constraint('ux_event_reviews_event_user', 'event_reviews', type_='unique')
    except Exception:
        pass
    op.drop_index('ix_event_reviews_userID', table_name='event_reviews')
    op.drop_index('ix_event_reviews_eventID', table_name='event_reviews')
    op.drop_table('event_reviews')

