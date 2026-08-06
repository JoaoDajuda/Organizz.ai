#criação do modelo de banco de dados

from sqlalchemy import create_engine, Column, String, Integer, Boolean, Float, ForeignKey, DateTime, func
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
    ativo = Column("ativo", Boolean, default=True)
    admin = Column("admin", Boolean, default=False)

    def __init__(self, nome, email, senha, ativo=True, admin=False):
        self.nome=nome
        self.email=email
        self.senha=senha
        self.ativo=ativo
        self.admin=admin         

class Valores(Base):
    __tablename__ = "movimentações"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    valor = Column("movimentação", Float)
    usuario = Column("usuario", ForeignKey("usuarios.id"))
    data_movimentacao = Column(DateTime(timezone=True), default=func.now())

    def __init__(self, valor, usuario):

        self.valor=valor
        self.usuario=usuario

class Atividades(Base):
    __tablename__ = "atividades"

    id = Column("id", Integer, primary_key= True, autoincrement=True)
    atividade = Column("atividade", String)
    usuario = Column("usuario", ForeignKey("usuarios.id"))
    concluido = Column("conclusao", DateTime)
    data_criacao = Column(DateTime(timezone=True), default=func.now())

    def __init__(self, valor, usuario):

        self.valor=valor
        self.valor=usuario