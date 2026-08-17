from fastapi import APIRouter, Depends, HTTPException
from schemas import UsuarioSchemas, LoginSchemas
from dependencies import pegar_sessao
from sqlalchemy.orm import Session
from main import bcrypt_context
from models import Usuario


auth_router = APIRouter(prefix="/auth", tags=["auth"])

def criar_token(id_usuario):
    token = f";plkoy54e3r{id_usuario}"
    return token

def autenticar_usuario(email, senha, session,):
    usuario = session.query(Usuario).filter(Usuario.email == email).first()
    if not usuario:
        return False
    elif not bcrypt_context.verify(senha, usuario.senha):
        return False
    return usuario

@auth_router.post("/criar_conta")
async def criar_conta(usuarioschemas: UsuarioSchemas, session: Session = Depends(pegar_sessao)):
    """essa rota é responsavel pela criação de usuário e comparação de email no banco de dados"""
    usuario = session.query(Usuario).filter(Usuario.email ==usuarioschemas.email).first()
    if usuario:
        raise HTTPException(status_code=400, detail="email já cadastrado")
    else:
        criptografia = bcrypt_context.hash(usuarioschemas.senha)
        novo_usuario = Usuario(usuarioschemas.nome, usuarioschemas.email, criptografia)
        session.add(novo_usuario)
        session.commit() 
        return{"mensagem":"email cadastrado com sucesso!"}

@auth_router.post("/fazer_login")
async def login(loginSchema: LoginSchemas, session: Session= Depends(pegar_sessao)):

    """essa rota é resposável por permitir a verificação e login do Usuário"""

    usuario = autenticar_usuario(loginSchema.email, loginSchema.senha, session)
    if not usuario:
        raise HTTPException(status_code=400, detail="Credenciais inválidas... tente novamente")

    else:
        acess_token = criar_token(Usuario.id)
        return{
            "acess_token" : acess_token,
            "type_token" : "Bearer"
        }
    