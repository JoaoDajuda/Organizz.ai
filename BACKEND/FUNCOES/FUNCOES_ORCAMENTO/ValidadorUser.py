from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from ..addonsSeguranca.config import SECRET_KEY, ALGORITHM, ACESS_TOKEN_EXPIRE


def criar_token(dados: dict, expira_em: timedelta = None):
    
    codificador = dados.copy()

    if expira_em:
        expira = datetime.now(timezone.utc) + expira_em

    else:
        expira = datetime.now(timezone.utc) + timedelta(minutes=ACESS_TOKEN_EXPIRE)

    codificador.update({"exp":expira})

    token_jwt= jwt.encode(codificador, SECRET_KEY, algorithm=ALGORITHM)
    return token_jwt

def verificar_token(token: str):
    #valida o jwte e retorna os dados se for valido.
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None