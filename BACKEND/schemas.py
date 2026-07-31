from pydantic import BaseModel
from typing import Optional

#parametros para a criação de usuários
class UsuarioSchemas(BaseModel):
    nome: str
    email: str
    senha: str
    ativo: Optional[bool]
    admin: Optional[bool]

    class config:
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