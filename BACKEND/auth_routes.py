from fastapi import APIRouter, Depends, HTTPException
from models import Usuario
from dependencies import pegar_sessao
from schemas import UsuarioSchemas, LoginSchemas
from sqlalchemy.orm import Session

auth_router = APIRouter(prefix="/auth", tags=["auth"])

@auth_router.post("/criar_conta")
async def criar_conta(usuarioschemas: UsuarioSchemas, session: Session = Depends(pegar_sessao)):
    usuario = session.query(Usuario).filter(Usuario.email ==usuarioschemas.email).first()
    if usuario:
        raise HTTPException(status_code=400, detail="email já cadastrado")
    else:
        novo_usuario = Usuario(usuarioschemas.nome, usuarioschemas.email, usuarioschemas.senha)

        session.add(novo_usuario)
        session.commit()
        session.close()
        session.close()
        return{"mensagem":"email cadastrado com sucesso!"}