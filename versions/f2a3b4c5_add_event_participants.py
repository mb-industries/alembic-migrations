"""add event_participants table to persist eligible reviewers

Revision ID: f2a3b4c5_add_event_participants
Revises: f1a2b3c4_merge_heads
Create Date: 2025-10-22 21:46:00
"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'f2a3b4c5_add_event_participants'
down_revision = 'f1a2b3c4_merge_heads'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'event_participants',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('eventID', sa.BigInteger, nullable=False),
        sa.Column('userID', sa.BigInteger, nullable=False),
    )
    op.create_index('ix_event_participants_eventID', 'event_participants', ['eventID'])
    try:
        op.create_unique_constraint('ux_event_participants_event_user', 'event_participants', ['eventID', 'userID'])
    except Exception:
        pass


def downgrade():
    try:
        op.drop_constraint('ux_event_participants_event_user', 'event_participants', type_='unique')
    except Exception:
        pass
    op.drop_index('ix_event_participants_eventID', table_name='event_participants')
    op.drop_table('event_participants')

