"""Add SubscriptionDuration Table for balance management with price removed

Revision ID: 425672dd2d92
Revises: 0cc4ce6093cd
Create Date: 2024-02-20 23:26:48.844809

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '425672dd2d92'
down_revision: Union[str, None] = '0cc4ce6093cd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
