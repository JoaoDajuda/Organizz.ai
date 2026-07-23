from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field

#modelo do body
class Loginrequest(BaseModel):
    usuario_id: str = Field(...,min_length=3, description="ID do Usuário")
    senha: str=Field(...,min_length=3, description="Senha do Usuário")

async def Autenticar(credenciais: Loginrequest):
    Saldo = 1
    #validando dados
    if credenciais.usuario_id == "admin" and credenciais.senha == "1234":
        #Se for verdadeiro, retorna o saldo
        return{"Saldo": Saldo}
    else:
        #Erro retornado
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas. Verifique o ID e a senha."
        )