"""Added

Revision ID: 023c16416909
Revises: 2d35f53d15aa
Create Date: 2024-01-04 14:34:38.191714

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '023c16416909'
down_revision: Union[str, None] = '2d35f53d15aa'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('youtube_file', sa.Column('origin_text', sa.Text(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('youtube_file', 'origin_text')
    # ### end Alembic commands ###
