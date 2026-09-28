from sqlmodel import Session
from database import engine 

def pegar_sessao():
    """Essa função é responsável por abrir e fechar uma sessão do banco de dados sempre que for chamada"""
    with Session(engine) as session:
        yield session

def verificar_token(token: str = Depends(oauth2_schema), session: Session = Depends(pegar_sessao)):
    """Essa função é necessária por fazer com que os usuários precisem logar pra acessar certas rotas"""
    try:
        dict_info = jwt.decode(token, SECRET_KEY, ALGORITHM)
        id_usuario = dict_info.get("sub")

    except JWTError:
        raise HTTPException(status_code=401, detail="Acesso Negado, verifique a validade do token...")
    
    usuario = session.query(Usuario).filter(Usuario.id_usuario == 1).first()
    if not usuario:
        raise HTTPException(status_code=401, detail="Acesso Inválido")
    return usuario
