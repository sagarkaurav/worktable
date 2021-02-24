"""add columns for reset password

Revision ID: 8bf296e747a1
Revises: 8a14eea67997
Create Date: 2021-02-24 05:52:44.496643

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "8bf296e747a1"
down_revision = "8a14eea67997"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "members",
        sa.Column("reset_password_token", sa.String(length=255), nullable=True),
    )
    op.add_column(
        "members",
        sa.Column("reset_password_token_created_at", sa.DateTime(), nullable=True),
    )
    op.add_column(
        "members",
        sa.Column("reset_password_token_valid_for", sa.Integer(), nullable=True),
    )
    op.create_unique_constraint(
        "members_reset_password_token_uniq_const", "members", ["reset_password_token"]
    )


def downgrade():
    op.drop_constraint(
        "members_reset_password_token_uniq_const", "members", type_="unique"
    )
    op.drop_column("members", "reset_password_token_valid_for")
    op.drop_column("members", "reset_password_token_created_at")
    op.drop_column("members", "reset_password_token")
