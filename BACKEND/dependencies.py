from models import db
from sqlalchemy.orm import sessionmaker

# Crie a fábrica de sessões FORA da função (uma única vez ao iniciar a app)
Session = sessionmaker(bind=db)

def pegar_sessao():
    """Essa função é responsável por abrir e fechar uma sessão do banco de dados sempre que for chamada"""
    
    session = Session()
    try:
        yield session
    finally:
        session.close()