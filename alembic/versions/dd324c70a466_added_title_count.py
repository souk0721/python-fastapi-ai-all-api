"""Added title_count

Revision ID: dd324c70a466
Revises: 4752241959bc
Create Date: 2024-01-10 09:19:14.124763

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'dd324c70a466'
down_revision: Union[str, None] = '4752241959bc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('youtube_file', sa.Column('gemini_title_tag_failed_count', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('youtube_file', 'gemini_title_tag_failed_count')
    # ### end Alembic commands ###
