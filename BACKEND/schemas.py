from pydantic import BaseModel
from typing import Optional
from pydantic import EmailStr

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
    data: str
    titulo: str
    rotina: str
    conclusao: bool
    class Config:
        from_attributes = True

class DeleteSchema(BaseModel):
    id_tarefa: int
    rotina: str
    id_usuario: str
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