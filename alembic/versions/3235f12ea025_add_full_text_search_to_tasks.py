"""add full text search to tasks

Revision ID: 3235f12ea025
Revises: 69fc7447097e
Create Date: 2026-05-13 15:08:22.243981

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3235f12ea025'
down_revision: Union[str, Sequence[str], None] = '69fc7447097e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    """Upgrade schema."""
    op.execute("""
        CREATE INDEX ix_tasks_search ON tasks
        USING GIN (to_tsvector('english', coalesce(title, '') || ' ' || coalesce(description, '')))
    """)


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("DROP INDEX IF EXISTS ix_tasks_search")