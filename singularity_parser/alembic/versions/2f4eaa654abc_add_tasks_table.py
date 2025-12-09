"""Add tasks table

Revision ID: 2f4eaa654abc
Revises: ceff537345f6
Create Date: 2025-12-10 01:32:42.753685

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '2f4eaa654abc'
down_revision: Union[str, Sequence[str], None] = 'ceff537345f6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'tasks',
        sa.Column('id', sa.Integer, nullable=False, primary_key=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()')),
        sa.Column('title', sa.VARCHAR, nullable=False),
        sa.Column('singularity_id', sa.VARCHAR, nullable=False),
        sa.Column('singularity_created_date', sa.DateTime, nullable=False),
        sa.Column('singularity_journal_date', sa.DateTime, nullable=True),
        sa.Column('singularity_delete_date', sa.DateTime, nullable=False),
        sa.Column('original_data', postgresql.JSONB())
    )


def downgrade() -> None:
    """Downgrade schema."""
    pass
