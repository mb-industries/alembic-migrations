"""Merge feedback extension and loadout manager heads

Revision ID: lm0002_merge_feedback_loadout
Revises: g4h5i6j7a8b_add_event_review_feedback_fields, lm0001_loadout_manager
Create Date: 2025-10-26 13:30:00
"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'lm0002_merge_feedback_loadout'
down_revision = ('g4h5i6j7a8b_add_event_review_feedback_fields', 'lm0001_loadout_manager')
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass

