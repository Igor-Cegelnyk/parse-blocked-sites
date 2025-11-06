"""remove unique constraint on domains

Revision ID: 512142016519
Revises: 746a8b40f579
Create Date: 2025-11-05 13:24:00.483769

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "512142016519"
down_revision: Union[str, Sequence[str], None] = "746a8b40f579"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.drop_constraint("uix_domain_blocklist", "domains", type_="unique")


def downgrade() -> None:
    """Downgrade schema."""
    op.create_unique_constraint(
        "uix_domain_blocklist", "domains", ["domain_name", "block_list"]
    )
