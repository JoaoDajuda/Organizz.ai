from fastapi import APIRouter, Depends
from models import Valores, Usuario
from sqlalchemy.orm import Session
from sqlalchemy import update
from dependencies import pegar_sessao
from schemas import EntradaSchema

math_router = APIRouter(prefix="/contas", tags=["contas"])
add_router = APIRouter(prefix="/soma", tags=["contas"])

@math_router.post("/adicao")
async def criar_input(entradaschema: EntradaSchema, session: Session = Depends(pegar_sessao)):
    """essa rota é reponsavel por criar o acesso as entradas de valores do usuário no banco de dados"""
    usuario = session.query(Usuario).filter(Usuario.id == entradaschema.id_usuario).first()
    if usuario:
        novo_input = Valores(
            usuario=entradaschema.id_usuario, 
            valor=entradaschema.valor
        )
        session.add(novo_input)
        session.commit()
        return {"mensagem": "entrada registrada com sucesso!"}
    else:
        return{"mensagem":{"id não cadastrado, tente novamente"}}

@add_router.patch("/soma")
async def soma(entradaschema: EntradaSchema, session: Session = Depends(pegar_sessao)):
    """Rota responsável por somar os valores solicitados no banco de dados"""
    usuario = session.query(Usuario).filter(Usuario.id == entradaschema.id_usuario).first()
    if usuario:

        registro = session.query(Valores).filter(Valores.usuario == entradaschema.id_usuario).order_by(Valores.id.desc()).first()

        valor_anterior = registro.valor

        if registro:
            adicao = valor_anterior + entradaschema.valor

            nova_movimentacao = Valores(valor= adicao, usuario=usuario.id)

            session.add(nova_movimentacao)
            session.commit()
        else:
            0.0
            return {"mensagem": "Novo registro criado com a soma com sucesso!"}
    return {"mensagem": "id não cadastrado, tente novamente"}
