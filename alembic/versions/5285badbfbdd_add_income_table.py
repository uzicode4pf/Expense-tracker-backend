"""add income table

Revision ID: 5285badbfbdd
Revises: 4c322d1d9c2b
Create Date: 2025-10-23 23:39:12.430566
"""

from typing import Sequence, Union
from datetime import datetime
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '5285badbfbdd'
down_revision: Union[str, Sequence[str], None] = '4c322d1d9c2b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Create income table only
    op.create_table(
        'income',
        sa.Column('id', sa.String(), primary_key=True, index=True),
        sa.Column('user_id', sa.String(), nullable=False),
        sa.Column('amount', sa.Float(), nullable=False),
        sa.Column('source', sa.String(), nullable=False),
        sa.Column('description', sa.String(), nullable=True),
        sa.Column('date', sa.DateTime(timezone=True), default=datetime.utcnow),
        sa.Column('created_at', sa.DateTime(timezone=True), default=datetime.utcnow),
    )


def downgrade() -> None:
    """Downgrade schema."""
    # Drop income table
    op.drop_table('income')