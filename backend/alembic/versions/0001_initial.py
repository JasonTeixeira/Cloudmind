"""Initial Alembic baseline

Revision ID: 0001_initial
Revises: 
Create Date: 2025-08-17

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "0001_initial"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Baseline migration. Generate real migrations with Alembic autogenerate.
    pass


def downgrade() -> None:
    # Baseline downgrade.
    pass


