"""tables

Revision ID: 983e221bb6b7
Revises: d090adc98a48
Create Date: 2024-02-16 14:51:17.668112

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '983e221bb6b7'
down_revision: Union[str, None] = 'd090adc98a48'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('sources',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('type', postgresql.ENUM('website', 'discord', name='source_type'), nullable=False),
    sa.Column('data', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('last_sync', sa.DateTime(), nullable=True),
    sa.Column('next_refresh', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('files',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('source_id', sa.UUID(), nullable=False),
    sa.Column('raw_content', sa.String(), nullable=False),
    sa.Column('markdown', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['source_id'], ['sources.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('files')
    op.drop_table('sources')
    # ### end Alembic commands ###
