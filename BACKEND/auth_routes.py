from fastapi import APIRouter, Depends, HTTPException
from main import bcrypt_context, ALGORITHM, TIMER, SECRET_KEY
from datetime import datetime,timedelta,timezone
from dependencies import pegar_sessao, verificar_token
from jose import jwt,JWTError
from sqlmodel import Session, select
from models import Usuario
from fastapi.security import OAuth2PasswordRequestForm
from schemas import UsuarioSchemas, LoginSchemas, SolicitarEmailSchema, ResetSenhaSchema
from email_utils import enviar_email

auth_router = APIRouter(prefix="/auth", tags=["auth"])

def criar_token_recuperacao(id_usuario):
    expira = datetime.now(timezone.utc) + timedelta(minutes=15)
    dict_info = {"sub": str(id_usuario), "exp": int(expira.timestamp()), "tipo": "recuperacao"}
    token = jwt.encode(dict_info, SECRET_KEY, ALGORITHM)
    return token


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
    usuario = autenticar_usuario(usuarioschemas.email, usuarioschemas.senha, session)

    if usuario:
        raise HTTPException(status_code=400, detail="email já cadastrado")

    else:
        criptografia = bcrypt_context.hash(usuarioschemas.senha)
        novo_usuario = Usuario(nome=usuarioschemas.nome,email=usuarioschemas.email,senha=criptografia, emailrec=usuarioschemas.emailrec,
        )
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
        acess_token = criar_token(usuario)
        refresh_token = criar_token(usuario, duracao_token = timedelta(days=7))
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
    acess_token = criar_token(usuario.id_usuario)
    return{
        "acess_token" : acess_token,
        "token_type" : "Bearer"
    }
    
@auth_router.post("/esqueci-senha")
async def esqueci_senha(dados: SolicitarEmailSchema, session: Session = Depends(pegar_sessao)):
    """essa rota é responsável por gerar e enviar o link de recuperação de senha"""
    usuario = session.query(Usuario).filter(Usuario.email == dados.email).first()

    if usuario:
        token = criar_token_recuperacao(usuario.id_usuario)
        link = f"http://localhost:3000/resetar-senha?token={token}"
        corpo = f"<p>Clique no link para redefinir sua senha (válido por 15 minutos):</p><a href='{link}'>{link}</a>"
        enviar_email(usuario.email, "Recuperação de senha - Organizz.ai", corpo)

    return {"mensagem": "Se o email estiver cadastrado, um link de recuperação de senha foi enviado."}

@auth_router.post("/resetar-senha")
async def resetar_senha(dados: ResetSenhaSchema, session: Session = Depends(pegar_sessao)):
    """essa rota é responsável por validar o token e atualizar a senha do usuário"""
    try:
        payload = jwt.decode(dados.token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get("tipo") != "recuperacao":
            raise HTTPException(status_code=400, detail="Token Inválido")
        id_usuario = int(payload.get("sub"))

    except JWTError:
        raise HTTPException(status_code=400, detail="Token Inválido")

    usuario = session.query(Usuario).filter(Usuario.id_usuario == id_usuario).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    usuario.senha = bcrypt_context.hash(dados.nova_senha)
    session.add(usuario)
    session.commit()

    return {"mensagem": "Senha atualizada com sucesso!"}