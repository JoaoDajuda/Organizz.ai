from pydantic import BaseModel
from typing import Optional

class UsuarioSchemas(BaseModel):
    nome: str
    email: str
    senha: str
    ativo: Optional[bool]
    admin: Optional[bool]

    class config:
        from_attributes = True


class LoginSchemas(BaseModel):
    email: str
    senha: str

    class Config:
        from_attributes = True

class EntradaSchema(BaseModel):
    id_usuario: str
    valor: bool

    class Config:
        from_attributes = True
    