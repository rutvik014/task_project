"""Merge heads e5438db0b40e and xxxx_merge_heads

Revision ID: 1330f5a3041d
Revises: e5438db0b40e, xxxx_merge_heads
Create Date: 2024-12-24 17:14:58.904477

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1330f5a3041d'
down_revision = ('e5438db0b40e', 'xxxx_merge_heads')
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass
