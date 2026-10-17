"""add per-user onboarding profile

Revision ID: a6f3b2c9d710
Revises: 5c5523a9c188
Create Date: 2026-10-17

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "a6f3b2c9d710"
down_revision: Union[str, Sequence[str], None] = "5c5523a9c188"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "perfil_onboarding",
        sa.Column("id_perfil", sa.Integer(), nullable=False),
        sa.Column("id_usuario", sa.Integer(), nullable=False),
        sa.Column("objetivo_financeiro", sa.String(length=300), nullable=False),
        sa.Column("faixa_renda_mensal", sa.String(length=32), nullable=False),
        sa.Column("faixa_despesas_mensais", sa.String(length=32), nullable=False),
        sa.Column("possui_dividas", sa.Boolean(), nullable=False),
        sa.Column("reserva_emergencia", sa.String(length=32), nullable=False),
        sa.Column("perfil_risco", sa.String(length=32), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["id_usuario"], ["usuario.id_usuario"]),
        sa.PrimaryKeyConstraint("id_perfil"),
        sa.UniqueConstraint("id_usuario"),
    )


def downgrade() -> None:
    op.drop_table("perfil_onboarding")