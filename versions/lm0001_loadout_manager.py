"""Loadout Manager initial tables

Revision ID: lm0001_loadout_manager
Revises: f3a4b5c6_add_event_review_events
Create Date: 2025-10-23
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'lm0001_loadout_manager'
down_revision: Union[str, None] = 'f3a4b5c6_add_event_review_events'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # lm_users
    op.create_table(
        'lm_users',
        sa.Column('id', sa.BigInteger(), primary_key=True),
        sa.Column('name', sa.Text(), nullable=True),
        sa.Column('username', sa.Text(), nullable=True),
        sa.Column('avatar_url', sa.Text(), nullable=True),
        sa.Column('admin', sa.Integer(), nullable=False, server_default='0'),
    )

    # lm_items
    op.create_table(
        'lm_items',
        sa.Column('id', sa.Text(), primary_key=True),
        sa.Column('name', sa.Text(), nullable=False),
        sa.Column('category', sa.Text(), nullable=False),
        sa.Column('manufacturer', sa.Text(), nullable=True),
        sa.Column('image_url', sa.Text(), nullable=True),
        sa.Column('stats_json', sa.Text(), nullable=True),
    )
    op.create_index('ix_lm_items_category', 'lm_items', ['category'])
    op.create_index('ix_lm_items_manufacturer', 'lm_items', ['manufacturer'])

    # taxonomy
    op.create_table(
        'lm_taxonomy_classes',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('value', sa.Text(), nullable=False, unique=True),
    )
    op.create_table(
        'lm_taxonomy_tags',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('value', sa.Text(), nullable=False, unique=True),
    )

    # loadouts
    op.create_table(
        'lm_loadouts',
        sa.Column('id', sa.Text(), primary_key=True),
        sa.Column('title', sa.Text(), nullable=False),
        sa.Column('class_value', sa.Text(), nullable=False),
        sa.Column('tags_json', sa.Text(), nullable=False, server_default='[]'),
        sa.Column('description', sa.Text(), nullable=False, server_default=''),
        sa.Column('images_json', sa.Text(), nullable=False, server_default='[]'),
        sa.Column('items_json', sa.Text(), nullable=True),
        sa.Column('custom_groups_json', sa.Text(), nullable=True),
        sa.Column('author_id', sa.BigInteger(), nullable=False),
        sa.Column('author_name', sa.Text(), nullable=True),
        sa.Column('author_username', sa.Text(), nullable=True),
        sa.Column('author_avatar_url', sa.Text(), nullable=True),
        sa.Column('private', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('org_advised', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('rating_avg', sa.Float(), nullable=False, server_default='0'),
        sa.Column('rating_count', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('created_at', sa.BigInteger(), nullable=False, server_default='0'),
        sa.Column('updated_at', sa.BigInteger(), nullable=False, server_default='0'),
        sa.Column('deleted', sa.Integer(), nullable=False, server_default='0'),
    )
    op.create_index('ix_lm_loadouts_author', 'lm_loadouts', ['author_id'])
    op.create_index('ix_lm_loadouts_created_at', 'lm_loadouts', ['created_at'])
    op.create_index('ix_lm_loadouts_class', 'lm_loadouts', ['class_value'])

    # ratings
    op.create_table(
        'lm_loadout_ratings',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('loadout_id', sa.Text(), nullable=False),
        sa.Column('user_id', sa.BigInteger(), nullable=False),
        sa.Column('value', sa.Integer(), nullable=False),
    )
    op.create_unique_constraint('ux_lm_rating_loadout_user', 'lm_loadout_ratings', ['loadout_id', 'user_id'])

    # saves
    op.create_table(
        'lm_saved_loadouts',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('loadout_id', sa.Text(), nullable=False),
        sa.Column('user_id', sa.BigInteger(), nullable=False),
        sa.Column('created_at', sa.BigInteger(), nullable=False, server_default='0'),
    )
    op.create_unique_constraint('ux_lm_saved_loadout_user', 'lm_saved_loadouts', ['loadout_id', 'user_id'])

    # shopping list
    op.create_table(
        'lm_shopping_list',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('user_id', sa.BigInteger(), nullable=False),
        sa.Column('item_id', sa.Text(), nullable=False),
        sa.Column('loadout_id', sa.Text(), nullable=True),
    )
    op.create_unique_constraint('ux_lm_shopping_user_item', 'lm_shopping_list', ['user_id', 'item_id'])

    # blocked
    op.create_table(
        'lm_blocked_public',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('user_id', sa.BigInteger(), nullable=False),
    )
    op.create_unique_constraint('ux_lm_blocked_user', 'lm_blocked_public', ['user_id'])


def downgrade() -> None:
    op.drop_constraint('ux_lm_blocked_user', 'lm_blocked_public', type_='unique')
    op.drop_table('lm_blocked_public')

    op.drop_constraint('ux_lm_shopping_user_item', 'lm_shopping_list', type_='unique')
    op.drop_table('lm_shopping_list')

    op.drop_constraint('ux_lm_saved_loadout_user', 'lm_saved_loadouts', type_='unique')
    op.drop_table('lm_saved_loadouts')

    op.drop_constraint('ux_lm_rating_loadout_user', 'lm_loadout_ratings', type_='unique')
    op.drop_table('lm_loadout_ratings')

    op.drop_index('ix_lm_loadouts_class', table_name='lm_loadouts')
    op.drop_index('ix_lm_loadouts_created_at', table_name='lm_loadouts')
    op.drop_index('ix_lm_loadouts_author', table_name='lm_loadouts')
    op.drop_table('lm_loadouts')

    op.drop_table('lm_taxonomy_tags')
    op.drop_table('lm_taxonomy_classes')

    op.drop_index('ix_lm_items_manufacturer', table_name='lm_items')
    op.drop_index('ix_lm_items_category', table_name='lm_items')
    op.drop_table('lm_items')

    op.drop_table('lm_users')

