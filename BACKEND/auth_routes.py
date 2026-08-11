from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from models import Usuario
from dependencies import pegar_sessao
from schemas import UsuarioSchemas, LoginSchemas
 
auth_router = APIRouter(prefix="/auth", tags=["auth"])
 
 
@auth_router.post("/criar_conta")
async def criar_conta(usuarioschemas: UsuarioSchemas, session: Session = Depends(pegar_sessao)):
    """essa rota é responsavel pela criação de usuário e comparação de email no banco de dados"""
    usuario = session.exec(
        select(Usuario).where(Usuario.email == usuarioschemas.email)
    ).first()
 
    if usuario:
        raise HTTPException(status_code=400, detail="email já cadastrado")
 
    novo_usuario = Usuario(
        nome=usuarioschemas.nome,
        email=usuarioschemas.email,
        senha=usuarioschemas.senha,
        emailrec=usuarioschemas.emailrec,
    )
 
    session.add(novo_usuario)
    session.commit()
    session.refresh(novo_usuario)
    return {"mensagem": "email cadastrado com sucesso!"}