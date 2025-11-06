"""fix unique constraint on domains

Revision ID: 746a8b40f579
Revises: 55c7fc341421
Create Date: 2025-11-05 12:50:12.550913

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "746a8b40f579"
down_revision: Union[str, Sequence[str], None] = "55c7fc341421"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_constraint("domains_domain_name_key", "domains", type_="unique")


def downgrade():
    op.create_unique_constraint("domains_domain_name_key", "domains", ["domain_name"])
