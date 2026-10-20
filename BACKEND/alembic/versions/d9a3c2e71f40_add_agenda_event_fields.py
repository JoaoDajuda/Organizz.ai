"""add calendar event fields to agenda

Revision ID: d9a3c2e71f40
Revises: a6f3b2c9d710
Create Date: 2026-10-19

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "d9a3c2e71f40"
down_revision: Union[str, Sequence[str], None] = "a6f3b2c9d710"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("agenda", sa.Column("data_fim", sa.String(length=64), nullable=True))
    op.add_column(
        "agenda",
        sa.Column("dia_inteiro", sa.Boolean(), server_default=sa.false(), nullable=False),
    )


def downgrade() -> None:
    op.drop_column("agenda", "dia_inteiro")
    op.drop_column("agenda", "data_fim")