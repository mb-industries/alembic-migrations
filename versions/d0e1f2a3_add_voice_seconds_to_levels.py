"""add VoiceSeconds to levels

Revision ID: d0e1f2a3
Revises: c9d1a2b3
Create Date: 2025-10-21 20:20:00
"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "d0e1f2a3"
down_revision = "c9d1a2b3"
branch_labels = None
depends_on = None


def upgrade():
    # Add integer column with default 0 so existing inserts continue to work
    op.add_column('levels', sa.Column('VoiceSeconds', sa.Integer(), nullable=False, server_default='0'))


def downgrade():
    op.drop_column('levels', 'VoiceSeconds')

