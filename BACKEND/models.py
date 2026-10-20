from typing import Optional
from sqlmodel import Field, SQLModel, Relationship
from enum import Enum
from datetime import datetime, timezone

# ENUMS
class StatusAgenda(str, Enum):
    pendente = "pendente"
    concluida = "concluida"
    atrasada = "atrasada"


class TipoTransacao(str, Enum):
    entrada = "Entrada"
    saida = "Saida"

# Entidades e atributos

class Usuario(SQLModel, table=True):
    id_usuario: Optional[int] = Field(default=None, primary_key=True)
    nome: str = Field(max_length=150, index=True)
    senha: str = Field(max_length=60)
    email: str = Field(max_length=200, index=True)
    emailrec: Optional[str] = Field(default=None, max_length=200)
    ativo: bool = Field(default=True)
    admin: bool = Field(default=False)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    deleted_at: Optional[datetime] = Field(default=None)
    codigo_recuperacao: Optional[str] = Field(default=None, max_length=6)
    codigo_recuperacao_expira: Optional[datetime] = Field(default=None)

    agendas: list["Agenda"] = Relationship(back_populates="usuario")
    valores: list["Valores"] = Relationship(back_populates="usuario")
    perfil_onboarding: Optional["PerfilOnboarding"] = Relationship(back_populates="usuario")


class PerfilOnboarding(SQLModel, table=True):
    __tablename__ = "perfil_onboarding"

    id_perfil: Optional[int] = Field(default=None, primary_key=True)
    id_usuario: int = Field(foreign_key="usuario.id_usuario", unique=True)
    objetivo_financeiro: str = Field(max_length=300)
    faixa_renda_mensal: str = Field(max_length=32)
    faixa_despesas_mensais: str = Field(max_length=32)
    possui_dividas: bool
    reserva_emergencia: str = Field(max_length=32)
    perfil_risco: str = Field(max_length=32)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    # Relacionamento
    usuario: Optional[Usuario] = Relationship(back_populates="perfil_onboarding")


class Agenda(SQLModel, table=True):
    id_agenda: Optional[int] = Field(default=None, primary_key=True)
    id_usuario: int = Field(foreign_key="usuario.id_usuario", index=True)
    titulo: str = Field(max_length=200)
    data: str = Field()
    data_fim: Optional[str] = Field(default=None, max_length=64)
    dia_inteiro: bool = Field(default=False)
    status: StatusAgenda = Field(default=StatusAgenda.pendente)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    deleted_at: Optional[datetime] = Field(default=None)

    # Relacionamento
    usuario: Optional[Usuario] = Relationship(back_populates="agendas")

class Valores(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    id_usuario: int = Field(foreign_key="usuario.id_usuario", index=True)
    tipo_valor: TipoTransacao = Field()
    valor: float = Field()
    saldo: Optional[float] = Field(default=0.0)
    data_movimentacao: datetime = Field(default_factory=datetime.utcnow)

    usuario: Optional[Usuario] = Relationship(back_populates="valores")