from fastapi import Depends, HTTPException
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from models import Usuario
from main import SECRET_KEY, ALGORITHM, oauth2_schema
from database import engine


def pegar_sessao():
    """Abre e fecha uma sessão do banco de dados sempre que for chamada"""
    with Session(engine) as session:
        yield session


def verificar_token(token: str = Depends(oauth2_schema), session: Session = Depends(pegar_sessao)):
    """Exige que o usuário esteja logado e devolve o usuário do token"""
    try:
        dict_info = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id_usuario = int(dict_info.get("sub"))
    except (JWTError, TypeError, ValueError):
        raise HTTPException(status_code=401, detail="Acesso Negado, verifique a validade do token...")

    usuario = session.query(Usuario).filter(Usuario.id_usuario == id_usuario).first()
    if not usuario:
        raise HTTPException(status_code=401, detail="Acesso Inválido")
    return usuario