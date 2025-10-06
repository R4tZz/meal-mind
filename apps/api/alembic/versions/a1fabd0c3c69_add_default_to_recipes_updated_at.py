"""add_default_to_recipes_updated_at

Revision ID: a1fabd0c3c69
Revises: 6942d77a42e3
Create Date: 2025-10-06 00:37:06.390662

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "a1fabd0c3c69"
down_revision: Union[str, Sequence[str], None] = "6942d77a42e3"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("ALTER TABLE recipes ALTER COLUMN updated_at SET DEFAULT now();")


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("ALTER TABLE recipes ALTER COLUMN updated_at DROP DEFAULT;")
