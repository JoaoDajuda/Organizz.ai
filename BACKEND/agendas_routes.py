from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from dependencies import pegar_sessao, verificar_token
from models import Agenda, StatusAgenda, Usuario
from schemas import AgendaCreateSchema, AgendaResponseSchema, AgendaStatusSchema

agenda_router = APIRouter(prefix="/agendas", tags=["agendas"])


@agenda_router.get("", response_model=list[AgendaResponseSchema])
def listar_agendas(
    usuario: Usuario = Depends(verificar_token),
    session: Session = Depends(pegar_sessao),
):
    return (
        session.query(Agenda)
        .filter(
            Agenda.id_usuario == usuario.id_usuario,
            Agenda.deleted_at.is_(None),
        )
        .order_by(Agenda.data, Agenda.id_agenda)
        .all()
    )


@agenda_router.post(
    "", response_model=AgendaResponseSchema, status_code=status.HTTP_201_CREATED
)
def criar_agenda(
    dados: AgendaCreateSchema,
    usuario: Usuario = Depends(verificar_token),
    session: Session = Depends(pegar_sessao),
):
    titulo = dados.titulo.strip()
    if not titulo:
        raise HTTPException(status_code=422, detail="O título da tarefa é obrigatório.")

    agenda = Agenda(
        id_usuario=usuario.id_usuario,
        titulo=titulo,
        data=dados.data,
        data_fim=dados.data_fim,
        dia_inteiro=dados.dia_inteiro,
    )
    session.add(agenda)
    session.commit()
    session.refresh(agenda)
    return agenda


@agenda_router.patch("/{id_agenda}", response_model=AgendaResponseSchema)
def atualizar_status_agenda(
    id_agenda: int,
    dados: AgendaStatusSchema,
    usuario: Usuario = Depends(verificar_token),
    session: Session = Depends(pegar_sessao),
):
    agenda = (
        session.query(Agenda)
        .filter(
            Agenda.id_agenda == id_agenda,
            Agenda.id_usuario == usuario.id_usuario,
            Agenda.deleted_at.is_(None),
        )
        .first()
    )
    if agenda is None:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada.")

    agenda.status = StatusAgenda(dados.status)
    session.commit()
    session.refresh(agenda)
    return agenda


@agenda_router.delete("/{id_agenda}", status_code=status.HTTP_204_NO_CONTENT)
def excluir_agenda(
    id_agenda: int,
    usuario: Usuario = Depends(verificar_token),
    session: Session = Depends(pegar_sessao),
):
    agenda = (
        session.query(Agenda)
        .filter(
            Agenda.id_agenda == id_agenda,
            Agenda.id_usuario == usuario.id_usuario,
            Agenda.deleted_at.is_(None),
        )
        .first()
    )
    if agenda is None:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada.")

    agenda.deleted_at = datetime.now(timezone.utc)
    session.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)