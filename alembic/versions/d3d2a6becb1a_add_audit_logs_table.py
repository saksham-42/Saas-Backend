"""add audit logs table

Revision ID: d3d2a6becb1a
Revises: 9c540ccd72b6
Create Date: 2026-05-15 18:31:06.835005

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd3d2a6becb1a'
down_revision: Union[str, Sequence[str], None] = '9c540ccd72b6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "audit_logs",
        sa.Column("id", sa.Integer, primary_key=True, index=True),
        sa.Column("user_id", sa.Integer, sa.ForeignKey("users.id", ondelete="SET NULL"), nullable=True),
        sa.Column("action", sa.String, nullable=False),
        sa.Column("resource", sa.String, nullable=False),
        sa.Column("resource_id", sa.Integer, nullable=True),
        sa.Column("org_id", sa.Integer, nullable=True),
        sa.Column("ip_address", sa.String, nullable=True),
        sa.Column("timestamp", sa.DateTime(timezone=True), nullable=False),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("audit_logs")
