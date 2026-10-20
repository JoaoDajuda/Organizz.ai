import random
import string
import logging
from datetime import datetime, timedelta
from uuid import uuid4
from fastapi import APIRouter, Depends, HTTPException
from main import bcrypt_context, ALGORITHM, TIMER, SECRET_KEY
from datetime import datetime,timedelta,timezone
from dependencies import pegar_sessao, verificar_token
from jose import jwt,JWTError
from sqlmodel import Session, select
from sqlalchemy.exc import IntegrityError, OperationalError, SQLAlchemyError, StatementError
from models import Usuario
from fastapi.security import OAuth2PasswordRequestForm
from schemas import UsuarioSchemas, LoginSchemas, SolicitarEmailSchema, ResetSenhaSchema
from email_utils import enviar_email

auth_router = APIRouter(prefix="/auth", tags=["auth"])
logger = logging.getLogger(__name__)


def _database_error_code(error):
    original_error = getattr(error, "orig", error)
    error_args = getattr(original_error, "args", ())
    if error_args and isinstance(error_args[0], int):
        return error_args[0]
    return None

def gerar_recuperacao() -> str:
    """Gera uma senha aleatória de 8 caracteres contendo letras e números."""
    caracteres = string.ascii_letters + string.digits
    senha_aleatoria = ''.join(random.choices(caracteres, k=6))
    return ''.join(random.choices(caracteres, k=6))

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
    request_id = uuid4().hex[:12]
    try:
        usuario = session.query(Usuario).filter(Usuario.email == usuarioschemas.email).first()
        if usuario:
            logger.warning("Cadastro recusado: email duplicado (request_id=%s)", request_id)
            raise HTTPException(
                status_code=400,
                detail="Email já cadastrado.",
                headers={
                    "X-Request-ID": request_id,
                    "X-Error-Code": "email_already_registered",
                },
            )

        criptografia = bcrypt_context.hash(usuarioschemas.senha)
        novo_usuario = Usuario(
            nome=usuarioschemas.nome,
            email=usuarioschemas.email,
            senha=criptografia,
            emailrec=usuarioschemas.emailrec,
        )
        session.add(novo_usuario)
        session.commit()
        logger.info("Cadastro concluído (request_id=%s)", request_id)
        return {"mensagem": "email cadastrado com sucesso!"}
    except HTTPException:
        raise
    except IntegrityError as error:
        session.rollback()
        error_code = _database_error_code(error)
        logger.warning(
            "Conflito de integridade no cadastro (request_id=%s, driver=%s, codigo=%s)",
            request_id,
            type(getattr(error, "orig", error)).__name__,
            error_code,
        )
        raise HTTPException(
            status_code=409,
            detail="Cadastro em conflito com um registro existente.",
            headers={
                "X-Request-ID": request_id,
                "X-Error-Code": "integrity_conflict",
            },
        ) from error
    except OperationalError as error:
        session.rollback()
        error_code = _database_error_code(error)
        logger.error(
            "Banco indisponível no cadastro (request_id=%s, driver=%s, codigo=%s)",
            request_id,
            type(getattr(error, "orig", error)).__name__,
            error_code,
        )
        raise HTTPException(
            status_code=503,
            detail="Banco indisponível para concluir o cadastro.",
            headers={
                "X-Request-ID": request_id,
                "X-Error-Code": "database_error",
            },
        ) from error
    except StatementError as error:
        session.rollback()
        root_error = getattr(error, "orig", error)
        logger.error(
            "Dados inválidos para persistência no cadastro (request_id=%s, tipo=%s)",
            request_id,
            type(root_error).__name__,
        )
        raise HTTPException(
            status_code=500,
            detail="Não foi possível preparar os dados do cadastro.",
            headers={
                "X-Request-ID": request_id,
                "X-Error-Code": "database_value_error",
            },
        ) from error
    except SQLAlchemyError as error:
        session.rollback()
        logger.error(
            "Falha SQLAlchemy no cadastro (request_id=%s, tipo=%s)",
            request_id,
            type(getattr(error, "orig", error)).__name__,
        )
        raise HTTPException(
            status_code=500,
            detail="Não foi possível salvar o cadastro.",
            headers={
                "X-Request-ID": request_id,
                "X-Error-Code": "database_operation_error",
            },
        ) from error
    except Exception as error:
        session.rollback()
        logger.error(
            "Falha inesperada no cadastro (request_id=%s, tipo=%s)",
            request_id,
            type(error).__name__,
        )
        raise HTTPException(
            status_code=500,
            detail="Erro interno ao concluir o cadastro.",
            headers={
                "X-Request-ID": request_id,
                "X-Error-Code": "internal_error",
            },
        ) from error

@auth_router.post("/fazer_login")
async def login(loginSchema: LoginSchemas, session: Session= Depends(pegar_sessao)):

    """essa rota é resposável por permitir a verificação e login do Usuário"""

    usuario = autenticar_usuario(loginSchema.email, loginSchema.senha, session)
    if not usuario:
        raise HTTPException(status_code=400, detail="Credenciais inválidas... tente novamente")

    else:
        acess_token = criar_token(usuario.id_usuario)
        refresh_token = criar_token(usuario.id_usuario, duracao_token=timedelta(days=7))
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
        acess_token = criar_token(usuario.id_usuario)
        refresh_token = criar_token(usuario.id_usuario, duracao_token = timedelta(days=7))
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
        codigo = gerar_recuperacao()
        usuario.codigo_recuperacao = codigo
        usuario.codigo_recuperacao_expira = datetime.utcnow() + timedelta(minutes=15)
        session.add(usuario)
        session.commit()

        corpo = f"<p>Seu código para redefinir sua senha (válido por 15 minutos) é:</p><h2>{codigo}</h2>"
        enviar_email(usuario.email, "Recuperação de senha - Organizz.ai", corpo)

    return {"mensagem": "Se o email estiver cadastrado, um link de recuperação de senha foi enviado."}


@auth_router.post("/resetar-senha")
async def resetar_senha(dados: ResetSenhaSchema, session: Session = Depends(pegar_sessao)):
    """essa rota é responsável por validar o código e atualizar a senha do usuário"""
    usuario = session.query(Usuario).filter(Usuario.email == dados.email).first()

    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    if not usuario.codigo_recuperacao or usuario.codigo_recuperacao != dados.codigo:
        raise HTTPException(status_code=400, detail="Código inválido")

    if usuario.codigo_recuperacao_expira < datetime.utcnow():
        raise HTTPException(status_code=400, detail="Código expirado")

    usuario.senha = bcrypt_context.hash(dados.nova_senha)
    usuario.codigo_recuperacao = None
    usuario.codigo_recuperacao_expira = None
    session.add(usuario)
    session.commit()

    return {"mensagem": "Senha atualizada com sucesso!"}