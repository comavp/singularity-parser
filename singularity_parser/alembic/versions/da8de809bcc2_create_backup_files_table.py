"""Create Backup Files table

Revision ID: da8de809bcc2
Revises: 
Create Date: 2025-12-06 18:24:10.272604

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'da8de809bcc2'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'backup_files',
        sa.Column('id', sa.Integer, nullable=False, primary_key=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()')),
        sa.Column('file_name', sa.VARCHAR, nullable=False),
        sa.Column('data', sa.Text, nullable=False),
        sa.Column('hash', sa.VARCHAR, nullable=False)
    )


def downgrade() -> None:
    op.drop_table('backup_files')
