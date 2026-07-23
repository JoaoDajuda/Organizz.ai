#criação do modelo de banco de dados

from sqlalchemy import create_engine, Column, String, Integer, Boolean, Float, ForeignKey
from sqlalchemy.orm import declarative_base

#cria a conexão com o banco

db = create_engine("sqlite:///banco.db")
Base = declarative_base()

#criar classes e tabelas no banco
class Usuario(Base):
    __tablename__  = "usuarios"

    id = Column("id", Integer, nullable= False, primary_key=True, autoincrement=True)
    nome = Column("nome", String)
    email = Column("email", String, nullable=False)
    senha = Column("senha", String)
    ativo = Column("ativo", String)
    admin = Column("admin", Boolean, default=False)

    def __init__(self, nome, email, senha, ativo=True, admin=False):
        self.nome=nome
        self.email=email
        self.senha=senha
        self.ativo=ativo
        self.admmin=admin         

class Valores(Base):
    __tablename__ = "movimentações"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    valor = Column("movimentação", Float)
    usuario = Column("usuario", ForeignKey("usuarios.id"))

    def __init__(self, valor, usuario):

        self.valor=valor
        self.usuario=usuario
