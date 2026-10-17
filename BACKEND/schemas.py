from pydantic import BaseModel
from typing import Literal, Optional
from pydantic import EmailStr, Field as SchemaField

#parametros para a criação de usuários
class UsuarioSchemas(BaseModel):
    nome: str
    email: str
    senha: str
    emailrec: Optional[str] = None
    ativo: Optional[bool]
    admin: Optional[bool]

    class Config:
        from_attributes = True


#parametros para login
class LoginSchemas(BaseModel):
    email: str
    senha: str

    class Config:
        from_attributes = True

#parametros para entrada de dados
class EntradaSchema(BaseModel):
    id_usuario: int
    valor: float

    class Config:
        from_attributes = True

class RotinaSchema(BaseModel):
    id_usuario: int
    rotina: str

    class Config:
        from_attributes = True

class SolicitarEmailSchema(BaseModel):
    email: EmailStr

    class Config:
        from_attributes = True

class ResetSenhaSchema(BaseModel):
    email: EmailStr
    codigo: str
    nova_senha: str

    class Config:
        from_attributes = True


class PerfilOnboardingSchema(BaseModel):
    objetivo_financeiro: str = SchemaField(min_length=3, max_length=300)
    faixa_renda_mensal: Literal[
        "ate_2000",
        "2001_5000",
        "5001_10000",
        "acima_10000",
        "prefiro_nao_informar",
    ]
    faixa_despesas_mensais: Literal[
        "ate_2000",
        "2001_5000",
        "5001_10000",
        "acima_10000",
        "prefiro_nao_informar",
    ]
    possui_dividas: bool
    reserva_emergencia: Literal[
        "nenhuma",
        "menos_1_mes",
        "1_3_meses",
        "mais_3_meses",
        "prefiro_nao_informar",
    ]
    perfil_risco: Literal["conservador", "moderado", "arrojado", "nao_sei"]


class EstadoOnboardingSchema(BaseModel):
    completed: bool
    profile: Optional[PerfilOnboardingSchema] = None