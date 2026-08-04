#criação do modelo de banco de dados
'''
from sqlalchemy import create_engine, Column, String, Integer, Boolean, Float, ForeignKey
from sqlalchemy.orm import declarative_base

#cria a conexão com o banco
###
db = create_engine("sqlite:///banco.db")
Base = declarative_base()

#criar classes e tabelas no banco
class Usuario(Base):
    __tablename__  = "usuarios"

    id = Column("id", Integer, nullable= False, primary_key=True, autoincrement=True)
    nome = Column("nome", String)
    email = Column("email", String, nullable=False)
    emailrec = Column("emailrec", String)
    senha = Column("senha", String)
    ativo = Column("ativo", Boolean, default=True)
    admin = Column("admin", Boolean, default=False)

    def __init__(self, nome, email, emailrec, senha, ativo=True, admin=False):
        self.nome=nome
        self.email=email
        self.emailrec=emailrec
        self.senha=senha
        self.ativo=ativo
        self.admin=admin         

class Valores(Base):
    __tablename__ = "movimentações"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    valor = Column("movimentação", Float)
    usuario = Column("usuario", ForeignKey("usuarios.id"))

    def __init__(self, valor, usuario):

        self.valor=valor
        self.usuario=usuario
'''
from typing import Optional
from sqlmodel import Field, SQLModel
from enum import Enum
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship

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
    senha: str = Field(max_length=30)
    email: str = Field(max_length=200, index=True)
    emailrec: str = Field(max_length=200)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    deleted_at: Optional[datetime] = Field(default=None)
    
    # Relacionamentos
    agendas: list["Agenda"] = Relationship(back_populates="usuario")
    financeiros: list["Financeiro"] = Relationship(back_populates="usuario")
    transacoes: list["Transacao"] = Relationship(back_populates="usuario")

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