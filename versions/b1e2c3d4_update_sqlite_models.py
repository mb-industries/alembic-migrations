"""update sqlite models: BigInteger IDs, soft relations, indexes

Revision ID: b1e2c3d4_update_sqlite_models
Revises: 7e9b6e6b8a1b_optimize_models
Create Date: 2025-10-16 00:00:00
"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "b1e2c3d4_update_sqlite_models"
down_revision = "7e9b6e6b8a1b_optimize_models"
branch_labels = None
depends_on = None


def upgrade():
    # Drop old tables if they exist (data loss acceptable)
    for t in [
        'league_records','league_banners','leagues',
        'delete_messages','suggestions','event_reminders','levels'
    ]:
        op.execute(sa.text(f'DROP TABLE IF EXISTS "{t}" CASCADE'))

    # Recreate tables with new schema
    op.create_table(
        'event_reminders',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('userID', sa.BigInteger, nullable=False),
        sa.Column('eventID', sa.BigInteger, nullable=False),
        sa.Column('remindAt', sa.BigInteger, nullable=False),
    )
    op.create_index('ix_event_reminders_userID', 'event_reminders', ['userID'])
    op.create_index('ix_event_reminders_eventID', 'event_reminders', ['eventID'])

    op.create_table(
        'suggestions',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('publicMessage', sa.BigInteger, nullable=False),
        sa.Column('privateMessage', sa.BigInteger, nullable=False),
        sa.Column('likes', sa.Text, nullable=False),
        sa.Column('dislikes', sa.Text, nullable=False),
        sa.Column('suggestion', sa.Text, nullable=False),
        sa.Column('author', sa.BigInteger, nullable=False),
        sa.Column('status', sa.Integer, nullable=False),
        sa.Column('timestamp', sa.BigInteger, nullable=False),
    )
    op.create_index('ix_suggestions_author', 'suggestions', ['author'])
    op.create_index('ix_suggestions_publicMessage', 'suggestions', ['publicMessage'])

    op.create_table(
        'delete_messages',
        sa.Column('message', sa.BigInteger, primary_key=True),
        sa.Column('user', sa.BigInteger, nullable=True),
        sa.Column('timestamp', sa.BigInteger, nullable=True),
    )
    op.create_index('ix_delete_messages_user', 'delete_messages', ['user'])

    op.create_table(
        'leagues',
        sa.Column('LeagueID', sa.Integer, primary_key=True),
        sa.Column('Name', sa.Text, nullable=False),
        sa.Column('CommandName', sa.Text, nullable=False),
        sa.Column('Active', sa.Integer, nullable=False, server_default='0'),
        sa.Column('Banner', sa.Text, nullable=False),
        sa.Column('IsTime', sa.Integer, nullable=False, server_default='0'),
    )

    op.create_table(
        'league_banners',
        sa.Column('Name', sa.Text, primary_key=True),
        sa.Column('Font', sa.Text, nullable=False),
        sa.Column('Cords', sa.Text, nullable=False),
        sa.Column('Color', sa.Text, nullable=True, server_default='#d9dbe1'),
    )

    op.create_table(
        'league_records',
        sa.Column('SubmissionID', sa.Integer, primary_key=True),
        sa.Column('UserID', sa.BigInteger, nullable=False),
        sa.Column('LeagueID', sa.Integer, sa.ForeignKey('leagues.LeagueID', ondelete='CASCADE'), nullable=False),
        sa.Column('Score', sa.Integer, nullable=False),
        sa.Column('Accepted', sa.Integer, nullable=False, server_default='0'),
    )
    op.create_index('ix_league_records_userID', 'league_records', ['UserID'])
    op.create_index('ix_league_records_LeagueID', 'league_records', ['LeagueID'])

    op.create_table(
        'levels',
        sa.Column('DiscordID', sa.BigInteger, primary_key=True),
        sa.Column('display_name', sa.Text, nullable=True),
        sa.Column('XP', sa.Integer, nullable=False, server_default='1'),
        sa.Column('Timestamp', sa.BigInteger, nullable=False, server_default='0'),
        sa.Column('LeagueGlobalScore', sa.Integer, nullable=False, server_default='0'),
    )


def downgrade():
    for t in [
        'league_records','league_banners','leagues',
        'delete_messages','suggestions','event_reminders','levels'
    ]:
        op.execute(sa.text(f'DROP TABLE IF EXISTS "{t}" CASCADE'))
