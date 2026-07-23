from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from dependencies import pegar_sessao
from schemas import EntradaSchema

order_routes = APIRouter(prefix="/contas", tags=["pedidos"])

@order_routes.post('/adicao')
async def criar_input(entradaschema: EntradaSchema, session: Session = Depends(pegar_sessao)):
    novo_input = entradas(usuario= entradaschema.id_usuario)
    session.add(novo_input)
    session.commit()
    return {"mensagem":"entrada registrada com sucesso!"}