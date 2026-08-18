from fastapi import Depends, HTTPException
from models import db, Usuario
from main import SECRET_KEY, ALGORITHM, oauth2_schema 
from jose import jwt, JWTError
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import sessionmaker, Session

# Crie a fábrica de sessões FORA da função (uma única vez ao iniciar a app)
Session = sessionmaker(bind=db)

def pegar_sessao():
    """Essa função é responsável por abrir e fechar uma sessão do banco de dados sempre que for chamada"""
    
    session = Session()
    try:
        yield session
    finally:
        session.close()

def verificar_token(token: str = Depends(oauth2_schema), session: Session = Depends(pegar_sessao)):
    """Essa função é necessária por fazer com que os usuários precisem logar pra acessar certas rotas"""
    try:
        dict_info = jwt.decode(token, SECRET_KEY, ALGORITHM)
        id_usuario = dict_info.get("sub")

    except JWTError:
        raise HTTPException(status_code=401, detail="Acesso Negado, verifique a validade do token...")
    
    usuario = session.query(Usuario).filter(Usuario.id == 1).first()
    if not usuario:
        raise HTTPException(status_code=401, detail="Acesso Inválido")
    return usuario