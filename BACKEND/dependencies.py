from sqlmodel import Session
from database import engine
 
 
def pegar_sessao():
    """Essa função é responsável por abrir e fechar uma sessão do banco de dados sempre que for chamada"""
 
    with Session(engine) as session:
        yield session