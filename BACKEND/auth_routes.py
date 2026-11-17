import secrets
import string
from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt
from sqlalchemy.orm import Session

from main import bcrypt_context, ALGORITHM, TIMER, SECRET_KEY
from dependencies import pegar_sessao, verificar_token
from models import Usuario
from schemas import UsuarioSchemas, LoginSchemas, SolicitarEmailSchema, ResetSenhaSchema
from email_utils import enviar_email

auth_router = APIRouter(prefix="/auth", tags=["auth"])


def gerar_recuperacao() -> str:
    """Gera um código aleatório de 6 caracteres com letras e números."""
    caracteres = string.ascii_letters + string.digits
    return "".join(secrets.choice(caracteres) for _ in range(6))


def criar_token(id_usuario, duracao_token=timedelta(minutes=TIMER)):
    expira = datetime.now(timezone.utc) + duracao_token
    dict_info = {"sub": str(id_usuario), "exp": int(expira.timestamp())}
    return jwt.encode(dict_info, SECRET_KEY, ALGORITHM)


def autenticar_usuario(email, senha, session):
    usuario = session.query(Usuario).filter(Usuario.email == email).first()
    if not usuario:
        return False
    if not bcrypt_context.verify(senha, usuario.senha):
        return False
    return usuario


def gerar_resposta_login(usuario):
    """Monta o retorno padrão do login (usado nas duas rotas de login)."""
    return {
        "access_token": criar_token(usuario.id_usuario),
        "refresh_token": criar_token(usuario.id_usuario, duracao_token=timedelta(days=7)),
        "token_type": "Bearer",
    }


@auth_router.post("/criar_conta")
def criar_conta(usuarioschemas: UsuarioSchemas, session: Session = Depends(pegar_sessao)):
    """Cria o usuário e verifica se o email já existe no banco de dados"""
    usuario = session.query(Usuario).filter(Usuario.email == usuarioschemas.email).first()
    if usuario:
        raise HTTPException(status_code=400, detail="email já cadastrado")

    novo_usuario = Usuario(
        nome=usuarioschemas.nome,
        email=usuarioschemas.email,
        senha=bcrypt_context.hash(usuarioschemas.senha),
        emailrec=usuarioschemas.emailrec,
    )
    session.add(novo_usuario)
    session.commit()
    return {"mensagem": "email cadastrado com sucesso!"}


@auth_router.post("/fazer_login")
def login(loginSchema: LoginSchemas, session: Session = Depends(pegar_sessao)):
    """Verifica as credenciais e faz o login do usuário"""
    usuario = autenticar_usuario(loginSchema.email, loginSchema.senha, session)
    if not usuario:
        raise HTTPException(status_code=400, detail="Credenciais inválidas... tente novamente")
    return gerar_resposta_login(usuario)


@auth_router.post("/login_form")
def login_form(
    dados_formulario: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(pegar_sessao),
):
    """Login usado pelo botão Authorize da documentação (Swagger)"""
    usuario = autenticar_usuario(dados_formulario.username, dados_formulario.password, session)
    if not usuario:
        raise HTTPException(status_code=400, detail="Credenciais inválidas... tente novamente")
    return gerar_resposta_login(usuario)


@auth_router.get("/refresh")
def use_refresh_token(usuario: Usuario = Depends(verificar_token)):
    return {
        "access_token": criar_token(usuario.id_usuario),
        "token_type": "Bearer",
    }


@auth_router.post("/esqueci-senha")
def esqueci_senha(dados: SolicitarEmailSchema, session: Session = Depends(pegar_sessao)):
    """Gera e envia o código de recuperação de senha"""
    usuario = session.query(Usuario).filter(Usuario.email == dados.email).first()

    if usuario:
        codigo = gerar_recuperacao()
        usuario.codigo_recuperacao = codigo
        usuario.codigo_recuperacao_expira = datetime.now(timezone.utc) + timedelta(minutes=15)
        session.add(usuario)
        session.commit()

        corpo = f"<p>Seu código para redefinir sua senha (válido por 15 minutos) é:</p><h2>{codigo}</h2>"
        enviar_email(usuario.email, "Recuperação de senha - Organizz.ai", corpo)

    return {"mensagem": "Se o email estiver cadastrado, um código de recuperação foi enviado."}


@auth_router.post("/resetar-senha")
def resetar_senha(dados: ResetSenhaSchema, session: Session = Depends(pegar_sessao)):
    """Valida o código e atualiza a senha do usuário"""
    usuario = session.query(Usuario).filter(Usuario.email == dados.email).first()

    if (
        not usuario
        or not usuario.codigo_recuperacao
        or not secrets.compare_digest(usuario.codigo_recuperacao, dados.codigo)
    ):
        raise HTTPException(status_code=400, detail="Código inválido")

    expira = usuario.codigo_recuperacao_expira
    if expira.tzinfo is None:  # banco guardou sem fuso horário
        expira = expira.replace(tzinfo=timezone.utc)
    if expira < datetime.now(timezone.utc):
        raise HTTPException(status_code=400, detail="Código expirado")

    usuario.senha = bcrypt_context.hash(dados.nova_senha)
    usuario.codigo_recuperacao = None
    usuario.codigo_recuperacao_expira = None
    session.add(usuario)
    session.commit()

    return {"mensagem": "Senha atualizada com sucesso!"}