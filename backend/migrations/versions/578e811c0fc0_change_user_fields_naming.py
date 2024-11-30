"""Change user fields naming

Revision ID: 578e811c0fc0
Revises: 19de8b2ee5e1
Create Date: 2024-11-24 23:24:14.219514

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '578e811c0fc0'
down_revision: Union[str, None] = '19de8b2ee5e1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Rename the columns instead of dropping them
    op.alter_column('user', 'firstName', new_column_name='first_name')
    op.alter_column('user', 'lastName', new_column_name='last_name')


def downgrade() -> None:
    # Revert the column names in case of a downgrade
    op.alter_column('user', 'first_name', new_column_name='firstName')
    op.alter_column('user', 'last_name', new_column_name='lastName')
