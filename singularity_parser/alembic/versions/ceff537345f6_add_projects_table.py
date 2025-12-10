"""Add projects table

Revision ID: ceff537345f6
Revises: d1c86802d25b
Create Date: 2025-12-10 01:13:42.135469

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'ceff537345f6'
down_revision: Union[str, Sequence[str], None] = 'd1c86802d25b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'projects',
        sa.Column('id', sa.VARCHAR, nullable=False, primary_key=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()')),
        sa.Column('title', sa.VARCHAR, nullable=False),
        sa.Column('singularity_created_date', sa.VARCHAR, nullable=True),
        sa.Column('singularity_journal_date', sa.DateTime, nullable=True),
        sa.Column('singularity_delete_date', sa.DateTime, nullable=True),
        sa.Column('original_data', postgresql.JSONB())
    )


def downgrade() -> None:
    op.drop_table('projects')
