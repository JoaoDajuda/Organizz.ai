from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from models import Usuario, Valores
from dependencies import pegar_sessao, verificar_token
from schemas import EntradaSchema

math_router = APIRouter(prefix="/contas", tags=["contas"])


def ultimo_saldo(session: Session, id_usuario: int) -> float:
    registro = (
        session.query(Valores)
        .filter(Valores.id_usuario == id_usuario)
        .order_by(Valores.id.desc())
        .first()
    )
    return registro.valor if registro else 0.0


@math_router.post("/adicao", status_code=201)
def criar_input(
    entrada: EntradaSchema,
    session: Session = Depends(pegar_sessao),
    usuario: Usuario = Depends(verificar_token),
):
    """Cria uma entrada de valor para o usuário autenticado."""
    novo_input = Valores(
        id_usuario=usuario.id_usuario,
        valor=entrada.valor,
        tipo_valor=entrada.tipo_valor,
    )
    session.add(novo_input)
    session.commit()
    return {"mensagem": "entrada registrada com sucesso!"}


@math_router.post("/soma", status_code=201)
def soma(
    entrada: EntradaSchema,
    session: Session = Depends(pegar_sessao),
    usuario: Usuario = Depends(verificar_token),
):
    """Soma o valor ao último saldo e cria um novo registro."""
    novo_valor = ultimo_saldo(session, usuario.id_usuario) + entrada.valor
    session.add(Valores(
        id_usuario=usuario.id_usuario,
        valor=novo_valor,
        tipo_valor=entrada.tipo_valor,
    ))
    session.commit()
    return {"mensagem": "Novo registro criado com sucesso!", "saldo": novo_valor}


@math_router.post("/subtracao", status_code=201)
def subtracao(
    entrada: EntradaSchema,
    session: Session = Depends(pegar_sessao),
    usuario: Usuario = Depends(verificar_token),
):
    """Subtrai o valor do último saldo e cria um novo registro."""
    novo_valor = ultimo_saldo(session, usuario.id_usuario) - entrada.valor
    session.add(Valores(
        id_usuario=usuario.id_usuario,
        valor=novo_valor,
        tipo_valor=entrada.tipo_valor,
    ))
    session.commit()
    return {"mensagem": "Registro criado com sucesso!", "saldo": novo_valor}


@math_router.get("/")
def listar_valores(
    session: Session = Depends(pegar_sessao),
    usuario: Usuario = Depends(verificar_token),
):
    """Lista os lançamentos do usuário autenticado."""
    registros = (
        session.query(Valores)
        .filter(Valores.id_usuario == usuario.id_usuario)
        .order_by(Valores.id.desc())
        .all()
    )
    return registros


@math_router.delete("/{id_valor}")
def deletar_valor(
    id_valor: int,
    session: Session = Depends(pegar_sessao),
    usuario: Usuario = Depends(verificar_token),
):
    """Exclui um lançamento, só se pertencer ao usuário autenticado."""
    registro = (
        session.query(Valores)
        .filter(Valores.id == id_valor, Valores.id_usuario == usuario.id_usuario)
        .first()
    )
    if not registro:
        raise HTTPException(status_code=404, detail="Lançamento não encontrado")
    session.delete(registro)
    session.commit()
    return {"mensagem": "Lançamento excluído com sucesso!"}