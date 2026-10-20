from datetime import datetime, timezone

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from dependencies import pegar_sessao, verificar_token
from models import PerfilOnboarding, Usuario
from schemas import EstadoOnboardingSchema, PerfilOnboardingSchema

onboarding_router = APIRouter(prefix="/onboarding", tags=["onboarding"])


@onboarding_router.get("", response_model=EstadoOnboardingSchema)
async def obter_onboarding(
    usuario: Usuario = Depends(verificar_token),
    session: Session = Depends(pegar_sessao),
):
    perfil = session.query(PerfilOnboarding).filter(
        PerfilOnboarding.id_usuario == usuario.id_usuario
    ).first()
    if perfil is None:
        return EstadoOnboardingSchema(completed=False)

    return EstadoOnboardingSchema(
        completed=True,
        profile=PerfilOnboardingSchema(**perfil.dict()),
    )


@onboarding_router.put("", response_model=EstadoOnboardingSchema)
async def salvar_onboarding(
    respostas: PerfilOnboardingSchema,
    usuario: Usuario = Depends(verificar_token),
    session: Session = Depends(pegar_sessao),
):
    perfil = session.query(PerfilOnboarding).filter(
        PerfilOnboarding.id_usuario == usuario.id_usuario
    ).first()
    dados = respostas.dict()

    if perfil is None:
        perfil = PerfilOnboarding(id_usuario=usuario.id_usuario, **dados)
    else:
        for campo, valor in dados.items():
            setattr(perfil, campo, valor)
        perfil.updated_at = datetime.now(timezone.utc)

    session.add(perfil)
    session.commit()
    session.refresh(perfil)

    return EstadoOnboardingSchema(
        completed=True,
        profile=PerfilOnboardingSchema(**perfil.dict()),
    )