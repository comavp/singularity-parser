"""Add jsonb column type to backup files table

Revision ID: d1c86802d25b
Revises: da8de809bcc2
Create Date: 2025-12-09 23:07:30.343370

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'd1c86802d25b'
down_revision: Union[str, Sequence[str], None] = 'da8de809bcc2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column(
        'backup_files',
        'data',
        existing_type=sa.TEXT(),
        type_=postgresql.JSONB(),
        postgresql_using='data::jsonb'
    )


def downgrade() -> None:
    op.alter_column(
        "backup_files",
        "data",
        existing_type=postgresql.JSONB,
        type_=sa.TEXT(),
        postgresql_using='data::text'
    )
