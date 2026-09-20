from typing import Optional
from sqlmodel import Field, SQLModel, Relationship
from enum import Enum
from datetime import datetime

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
    created_at: datetime = Field(default_factory=datetime.utcnow)
    deleted_at: Optional[datetime] = Field(default=None)
    codigo_recuperacao: Optional[str] = Field(default=None, max_length=6)
    codigo_recuperacao_expira: Optional[datetime] = Field(default=None)

    # Relacionamentos
    agendas: list["Agenda"] = Relationship(back_populates="usuario")
    financeiros: list["Financeiro"] = Relationship(back_populates="usuario")
    transacoes: list["Transacao"] = Relationship(back_populates="usuario")
    valores: list["Valores"] = Relationship(back_populates="usuario")


class Agenda(SQLModel, table=True):
    id_agenda: Optional[int] = Field(default=None, primary_key=True)
    id_usuario: int = Field(foreign_key="usuario.id_usuario", index=True)
    titulo: str = Field(max_length=200)
    data: str = Field()
    status: StatusAgenda = Field(default=StatusAgenda.pendente)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    deleted_at: Optional[datetime] = Field(default=None)

    # Relacionamento
    usuario: Optional[Usuario] = Relationship(back_populates="agendas")


class Financeiro(SQLModel, table=True):
    id_financeiro: Optional[int] = Field(default=None, primary_key=True)
    id_usuario: int = Field(foreign_key="usuario.id_usuario", index=True)
    saldo: float = Field(default=0.0)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    deleted_at: Optional[datetime] = Field(default=None)

    # Relacionamentos
    usuario: Optional[Usuario] = Relationship(back_populates="financeiros")
    transacoes: list["Transacao"] = Relationship(back_populates="financeiro")


class Transacao(SQLModel, table=True):
    id_transacoes: Optional[int] = Field(default=None, primary_key=True)
    id_usuario: int = Field(foreign_key="usuario.id_usuario", index=True)
    id_financeiro: int = Field(foreign_key="financeiro.id_financeiro", index=True)
    valor: float = Field()
    tipo: TipoTransacao
    data_mov: datetime = Field(default_factory=datetime.utcnow)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    deleted_at: Optional[datetime] = Field(default=None)

    # Relacionamentos
    usuario: Optional[Usuario] = Relationship(back_populates="transacoes")
    financeiro: Optional[Financeiro] = Relationship(back_populates="transacoes")

class Valores(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    id_usuario: int = Field(foreign_key="usuario.id_usuario", index=True)
    valor: float = Field()
    saldo: Optional[float] = Field(default=0.0)
    data_movimentacao: datetime = Field(default_factory=datetime.utcnow)

    usuario: Optional[Usuario] = Relationship(back_populates="valores")