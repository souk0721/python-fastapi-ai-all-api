"""Added whisper

Revision ID: 168c820826c3
Revises: 023c16416909
Create Date: 2024-01-04 22:07:27.483822

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '168c820826c3'
down_revision: Union[str, None] = '023c16416909'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('youtube_file', sa.Column('whisper_json', sa.JSON(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('youtube_file', 'whisper_json')
    # ### end Alembic commands ###