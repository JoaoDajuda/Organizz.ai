from sqlmodel import Field, Session, SQLModel, create_engine, select
from typing import Optional, List, Annotated
from datetime import datetime
from enum import Enum
from sqlalchemy import create_engine
from sqlmodel import SQLModel, Field, Relationship, Session
from fastapi import FastAPI, Depends,  HTTPException, Query

sqlite_file_name = "organizzai.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]

app = FastAPI()

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
    user_nome: str = Field(max_length=150, index=True)
    user_senha: str = Field(max_length=30)
    user_email: str = Field(max_length=200, index=True)
    user_emailrec: str = Field(max_length=200)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    deleted_at: Optional[datetime] = Field(default=None)
    
    # Relacionamentos
    agendas: List["Agenda"] = Relationship(back_populates="usuario")
    financeiros: List["Financeiro"] = Relationship(back_populates="usuario")
    transacoes: List["Transacao"] = Relationship(back_populates="usuario")

class Agenda(SQLModel, table=True):
    id_agenda: Optional[int] = Field(default=None, primary_key=True)
    id_usuario: int = Field(foreign_key="usuario.id_usuario", index=True)
    agen_titulo: str = Field(max_length=200)
    agen_data: str = Field()  
    agen_status: StatusAgenda = Field(default=StatusAgenda.pendente)
    
    # Relacionamento
    usuario: Optional[Usuario] = Relationship(back_populates="agendas")

class Financeiro(SQLModel, table=True):
    id_financeiro: Optional[int] = Field(default=None, primary_key=True)
    id_usuario: int = Field(foreign_key="usuario.id_usuario", index=True)
    fin_saldo: float = Field(default=0.0)
    
    # Relacionamentos
    usuario: Optional[Usuario] = Relationship(back_populates="financeiros")
    transacoes: List["Transacao"] = Relationship(back_populates="financeiro")

class Transacao(SQLModel, table=True):
    id_transacoes: Optional[int] = Field(default=None, primary_key=True)
    id_usuario: int = Field(foreign_key="usuario.id_usuario", index=True)
    id_financeiro: int = Field(foreign_key="financeiro.id_financeiro", index=True)
    tran_valor: float = Field()
    tran_tipo: TipoTransacao
    tran_datamov: datetime = Field(default_factory=datetime.utcnow)
    
    # Relacionamentos
    usuario: Optional[Usuario] = Relationship(back_populates="transacoes")
    financeiro: Optional[Financeiro] = Relationship(back_populates="transacoes")

@app.on_event("startup")
def on_startup():
    create_db_and_tables()