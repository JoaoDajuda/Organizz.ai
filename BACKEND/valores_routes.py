from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from dependencies import pegar_sessao, verificar_token
from models import TipoTransacao, Usuario, Valores
from schemas import ValoresCreateSchema, ValoresResponseSchema

valores_router = APIRouter(prefix="/valores", tags=["valores"])


@valores_router.get("", response_model=list[ValoresResponseSchema])
def listar_valores(
    usuario: Usuario = Depends(verificar_token),
    session: Session = Depends(pegar_sessao),
):
    return (
        session.query(Valores)
        .filter(Valores.id_usuario == usuario.id_usuario)
        .order_by(Valores.data_movimentacao.desc(), Valores.id.desc())
        .all()
    )


@valores_router.post(
    "", response_model=ValoresResponseSchema, status_code=status.HTTP_201_CREATED
)
def criar_valor(
    dados: ValoresCreateSchema,
    usuario: Usuario = Depends(verificar_token),
    session: Session = Depends(pegar_sessao),
):
    categoria = (dados.categoria or "").strip()
    tipo = TipoTransacao(dados.tipo_valor)

    if tipo == TipoTransacao.saida and not categoria:
        raise HTTPException(
            status_code=422, detail="Informe o tipo de gasto para uma saída."
        )

    data_movimentacao = datetime.now(timezone.utc)
    if dados.data:
        try:
            data_movimentacao = datetime.fromisoformat(dados.data).replace(tzinfo=timezone.utc)
        except ValueError:
            raise HTTPException(
                status_code=422, detail="Data inválida. Use o formato AAAA-MM-DD."
            )

    valor = Valores(
        id_usuario=usuario.id_usuario,
        tipo_valor=tipo,
        valor=dados.valor,
        categoria=categoria or None,
        data_movimentacao=data_movimentacao,
    )
    session.add(valor)
    session.commit()
    session.refresh(valor)
    return valor


@valores_router.delete("/{id_valor}", status_code=status.HTTP_204_NO_CONTENT)
def excluir_valor(
    id_valor: int,
    usuario: Usuario = Depends(verificar_token),
    session: Session = Depends(pegar_sessao),
):
    valor = (
        session.query(Valores)
        .filter(
            Valores.id == id_valor,
            Valores.id_usuario == usuario.id_usuario,
        )
        .first()
    )
    if valor is None:
        raise HTTPException(status_code=404, detail="Movimentação não encontrada.")

    session.delete(valor)
    session.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
