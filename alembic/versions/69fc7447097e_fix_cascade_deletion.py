"""fix cascade deletion

Revision ID: 69fc7447097e
Revises: 42c1a792ed02
Create Date: 2026-04-08 20:34:48.131681

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '69fc7447097e'
down_revision: Union[str, Sequence[str], None] = '42c1a792ed02'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.drop_constraint('organization_members_user_id_fkey','organization_members',type_='foreignkey')

    op.create_foreign_key('organization_members_user_id_fkey','organization_members','users',['user_id'],['id'],ondelete='CASCADE')

def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint('organization_members_user_id_fkey','organization_members',type_='foreignkey')

    op.create_foreign_key('organization_members_user_id_fkey','organization_members','users',['user_id'],['id'])
