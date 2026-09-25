from fastapi import APIRouter, Depends
from models import Agenda, Usuario
from sqlalchemy.orm import Session
from sqlalchemy import update
from dependencies import pegar_sessao
from schemas import RotinaSchema, DeleteSchema
from passlib.context import CryptContext

act_router = APIRouter(prefix="/acoes", tags= ["acoes"])

@act_router.post("/criacao")
async def criar_rotina(rotina_schema: RotinaSchema, session: Session = Depends(pegar_sessao)):
    """essa rota é responsavel por criar  uma nova rotina no banco de dados"""
    usuario = session.query(Usuario).filter(Usuario.id_usuario == rotina_schema.id_usuario).first()
    if usuario:
        nova_rotina = Agenda(id_usuario=rotina_schema.id_usuario, atividade=rotina_schema.rotina, data=rotina_schema.data, concluido=rotina_schema.conclusao, titulo=rotina_schema.titulo
        )
        session.add(nova_rotina)
        session.commit()
        return{"mensagem":"rotina criada com sucesso!!"}
    else:
        return{"mensagem":"id não cafastrado, tente novamente"}

@act_router.delete("/deletar")
async def deletar_rotina(dados: DeleteSchema, session: Session = Depends(pegar_sessao)):
    """essa rota é responsavel por deletar  uma nova rotina no banco de dados"""
    tarefa = session.query(Agenda).filter(
        Agenda.id_agenda == dados.id_tarefa,
        Agenda.id_usuario == dados.id_usuario
    ).first()

    if tarefa:
        nome = tarefa.titulo
        session.delete(tarefa)
        session.commit()
        return {"mensagem": f"Atividade '{nome}' excluída com sucesso"}
    else:
        return {"mensagem": "tarefa não encontrada"}