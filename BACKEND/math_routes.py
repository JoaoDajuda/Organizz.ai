from fastapi import APIRouter, Depends
from models import Valores, Usuario
from sqlalchemy.orm import Session
from dependencies import pegar_sessao
from schemas import EntradaSchema

math_router = APIRouter(prefix="/contas", tags=["contas"])

@math_router.post("/adicao")
async def criar_input(entradaschema: EntradaSchema, session: Session = Depends(pegar_sessao)):
    """essa rota é reponsavel por criar o acesso as entradas de valores do usuário no banco de dados"""
    usuario = session.query(Usuario).filter(usuario.id == entradaschema.id_usuario).first()
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