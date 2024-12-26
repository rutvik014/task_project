"""merge heads

Revision ID: xxxx_merge_heads
Revises: d97485b7f51c, xxxx_add_email_to_user
Create Date: 2024-12-24 16:30:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'xxxx_merge_heads'
down_revision = ('d97485b7f51c', 'xxxx_add_email_to_user')
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass
