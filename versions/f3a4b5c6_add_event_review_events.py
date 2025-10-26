"""add event_review_events to store event names and times

Revision ID: f3a4b5c6_add_event_review_events
Revises: f2a3b4c5_add_event_participants
Create Date: 2025-10-22 22:00:00
"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'f3a4b5c6_add_event_review_events'
down_revision = 'f2a3b4c5_add_event_participants'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'event_review_events',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('eventID', sa.BigInteger, nullable=False),
        sa.Column('name', sa.Text, nullable=True),
        sa.Column('start_ts', sa.BigInteger, nullable=True),
        sa.Column('end_ts', sa.BigInteger, nullable=True),
        sa.Column('closes_at', sa.BigInteger, nullable=True),
        sa.Column('message_id', sa.BigInteger, nullable=True),
    )
    op.create_unique_constraint('ux_event_review_events_eventID', 'event_review_events', ['eventID'])
    op.create_index('ix_event_review_events_closes_at', 'event_review_events', ['closes_at'])


def downgrade():
    try:
        op.drop_constraint('ux_event_review_events_eventID', 'event_review_events', type_='unique')
    except Exception:
        pass
    op.drop_index('ix_event_review_events_closes_at', table_name='event_review_events')
    op.drop_table('event_review_events')

