from fastapi import Depends, HTTPException
from models import Usuario
from main import SECRET_KEY, ALGORITHM, oauth2_schema 
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from database import engine

def pegar_sessao():
    """Essa função é responsável por abrir e fechar uma sessão do banco de dados sempre que for chamada"""

    with Session(engine) as session:
        yield session

def verificar_token(token: str = Depends(oauth2_schema), session: Session = Depends(pegar_sessao)):
    """Essa função é necessária por fazer com que os usuários precisem logar pra acessar certas rotas"""
    try:
        dict_info = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id_usuario = int(dict_info.get("sub"))
    except (JWTError, TypeError, ValueError):
        raise HTTPException(status_code=401, detail="Acesso Negado, verifique a validade do token...")

    usuario = session.get(Usuario, id_usuario)
    if not usuario:
        raise HTTPException(status_code=401, detail="Acesso Inválido")
    return usuario