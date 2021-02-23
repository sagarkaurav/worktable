"""add disabled_at column to members table

Revision ID: 8a14eea67997
Revises: 2561ab0178ea
Create Date: 2021-02-23 06:10:36.602906

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "8a14eea67997"
down_revision = "2561ab0178ea"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("members", sa.Column("disabled_at", sa.DateTime(), nullable=True))


def downgrade():
    op.drop_column("members", "disabled_at")
