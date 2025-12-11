"""Make singualirty dates in tasks table nullable

Revision ID: 858e2bcc1387
Revises: 2f4eaa654abc
Create Date: 2025-12-12 00:22:37.142586

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '858e2bcc1387'
down_revision: Union[str, Sequence[str], None] = '2f4eaa654abc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column(
        'tasks',
        'singularity_created_date',
        existing_type=sa.DateTime,
        nullable=True
    )
    op.alter_column(
        'tasks',
        'singularity_delete_date',
        existing_type=sa.DateTime,
        nullable=True
    )


def downgrade() -> None:
    op.execute("""
        UPDATE tasks
        SET singularity_created_date = CURRENT_TIMESTAMP
        WHERE singularity_created_date IS NULL
    """)
    op.execute("""
        UPDATE tasks 
        SET singularity_delete_date = CURRENT_TIMESTAMP 
        WHERE singularity_delete_date IS NULL
    """)
    op.alter_column(
        'tasks',
        'singularity_created_date',
        existing_type=sa.DateTime,
        nullable=False
    )
    op.alter_column(
        'tasks',
        'singularity_delete_date',
        existing_type=sa.DateTime,
        nullable=False
    )
