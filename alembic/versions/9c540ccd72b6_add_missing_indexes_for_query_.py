"""add missing indexes for query optimization

Revision ID: 9c540ccd72b6
Revises: 3235f12ea025
Create Date: 2026-05-13 21:06:21.964484

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9c540ccd72b6'
down_revision: Union[str, Sequence[str], None] = '3235f12ea025'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("CREATE INDEX IF NOT EXISTS ix_tasks_org_id ON tasks(org_id)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_tasks_assigned_to ON tasks(assigned_to)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_organization_members_org_id ON organization_members(org_id)")


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index('ix_tasks_org_id', table_name='tasks')
    op.drop_index('ix_tasks_assigned_to', table_name='tasks')
    op.drop_index('ix_organization_members_org_id', table_name='organization_members')