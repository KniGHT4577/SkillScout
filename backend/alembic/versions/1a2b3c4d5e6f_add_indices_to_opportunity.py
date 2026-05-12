"""add indices to opportunity

Revision ID: 1a2b3c4d5e6f
Revises: 0160d3cdb3d7
Create Date: 2025-05-15 10:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1a2b3c4d5e6f'
down_revision: Union[str, None] = '0160d3cdb3d7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_index(op.f('ix_opportunities_provider'), 'opportunities', ['provider'], unique=False)
    op.create_index(op.f('ix_opportunities_category'), 'opportunities', ['category'], unique=False)
    op.create_index(op.f('ix_opportunities_is_free'), 'opportunities', ['is_free'], unique=False)
    op.create_index(op.f('ix_opportunities_difficulty'), 'opportunities', ['difficulty'], unique=False)
    op.create_index(op.f('ix_opportunities_created_at'), 'opportunities', ['created_at'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_opportunities_created_at'), table_name='opportunities')
    op.drop_index(op.f('ix_opportunities_difficulty'), table_name='opportunities')
    op.drop_index(op.f('ix_opportunities_is_free'), table_name='opportunities')
    op.drop_index(op.f('ix_opportunities_category'), table_name='opportunities')
    op.drop_index(op.f('ix_opportunities_provider'), table_name='opportunities')
