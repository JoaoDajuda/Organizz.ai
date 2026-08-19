from fastapi import APIRouter, Depends, HTTPException
from main import bcrypt_context, ALGORITHM, TIMER, SECRET_KEY
from schemas import UsuarioSchemas, LoginSchemas
from datetime import datetime,timedelta,timezone
from dependencies import pegar_sessao, verificar_token 
from jose import jwt,JWTError
from sqlalchemy.orm import Session
from models import Usuario
from fastapi.security import OAuth2PasswordRequestForm


auth_router = APIRouter(prefix="/auth", tags=["auth"])

def criar_token(id_usuario, duracao_token=timedelta(minutes=TIMER)):
    expira = datetime.now(timezone.utc) + duracao_token
    dict_info = {"sub": str(id_usuario),"exp": int(expira.timestamp())}
    token = jwt.encode(dict_info, SECRET_KEY, ALGORITHM)
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
        acess_token = criar_token(usuario.id)
        refresh_token = criar_token(usuario.id, duracao_token = timedelta(days=7))
        return{
            "acess_token" : acess_token,
            "refresh_token" : refresh_token,
            "type_token" : "Bearer"
        }

@auth_router.post("/login_form")
async def login_form(dados_formulario: OAuth2PasswordRequestForm = Depends(), session: Session= Depends(pegar_sessao)):

    """essa rota é resposável por permitir a verificação e login do Usuário na documentação da API"""

    usuario = autenticar_usuario(dados_formulario.username, dados_formulario.password, session)
    if not usuario:
        raise HTTPException(status_code=400, detail="Credenciais inválidas... tente novamente")

    else:
        acess_token = criar_token(usuario.id)
        refresh_token = criar_token(usuario.id, duracao_token = timedelta(days=7))
        return{
            "acess_token" : acess_token,
            "refresh_token" : refresh_token,
            "type_token" : "Bearer"
        }

@auth_router.get("/refresh")
async def use_refresh_token(usuario : Usuario = Depends(verificar_token)):
    acess_token = criar_token(usuario.id)
    return{
        "acess_token" : acess_token,
        "token_type" : "Bearer"
    }
    