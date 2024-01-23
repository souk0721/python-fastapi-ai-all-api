"""Added

Revision ID: 2d35f53d15aa
Revises: 4b2f03b05142
Create Date: 2024-01-04 14:32:29.063373

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2d35f53d15aa'
down_revision: Union[str, None] = '4b2f03b05142'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('youtube_file', sa.Column('is_gemini', sa.Boolean(), nullable=False))
    op.add_column('youtube_file', sa.Column('gpt', sa.JSON(), nullable=True))
    op.add_column('youtube_file', sa.Column('gemini', sa.JSON(), nullable=True))
    op.add_column('youtube_file', sa.Column('notion', sa.JSON(), nullable=True))
    op.drop_column('youtube_file', 'is_geminai')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('youtube_file', sa.Column('is_geminai', sa.BOOLEAN(), autoincrement=False, nullable=False))
    op.drop_column('youtube_file', 'notion')
    op.drop_column('youtube_file', 'gemini')
    op.drop_column('youtube_file', 'gpt')
    op.drop_column('youtube_file', 'is_gemini')
    # ### end Alembic commands ###
