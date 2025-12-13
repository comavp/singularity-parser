"""Add modificated date column

Revision ID: 12b9aa97f394
Revises: 858e2bcc1387
Create Date: 2025-12-13 01:06:29.730381

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '12b9aa97f394'
down_revision: Union[str, Sequence[str], None] = '858e2bcc1387'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        'projects',
        sa.Column('singularity_modificated_date', sa.BIGINT, nullable=False)
    )
    op.add_column(
        'tasks',
        sa.Column('singularity_modificated_date', sa.BIGINT, nullable=False)
    )


def downgrade() -> None:
    op.drop_column('projects', 'singularity_modificated_date')
    op.drop_column('tasks', 'singularity_modificated_date')
