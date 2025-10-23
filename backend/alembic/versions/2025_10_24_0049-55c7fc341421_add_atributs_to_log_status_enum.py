"""Add atributs to log_status_enum

Revision ID: 55c7fc341421
Revises: 0d777eac4398
Create Date: 2025-10-24 00:49:05.988778

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "55c7fc341421"
down_revision: Union[str, Sequence[str], None] = "0d777eac4398"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("ALTER TYPE logstatusenum ADD VALUE IF NOT EXISTS 'NO_CHANGES';")


def downgrade() -> None:
    """Downgrade schema."""
    pass
