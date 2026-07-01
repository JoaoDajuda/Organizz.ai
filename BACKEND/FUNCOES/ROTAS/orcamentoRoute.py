from fastapi import FastAPI, APIRouter,HTTPException, status
from pydantic import BaseModel, Field

from ..FUNCOES_ORCAMENTO.saldo import versaldo
from ..FUNCOES_ORCAMENTO.soma import addvalor_v2
from ..FUNCOES_ORCAMENTO.subtracao import subvalor_v2
from ..FUNCOES_ORCAMENTO.ValidadorUser import criar_token

class OrcamentoRequest(BaseModel):
    valor: float

app = FastAPI()

# rota para somar valores e enviar ao banco
@app.get("/soma/{valor}")
async def somar(valor: float):
    resultado = addvalor_v2(valor)
    return resultado


# rota para subtrair valores e enviar ao banco
@app.get("/subtracao/{valor}")
async def subtrair(valor: float):
    resultado = subvalor_v2(valor)
    return resultado

@app.get("/saldo")
async def versaldo():
    saldo = versaldo()
    return saldo

@app.get("/")
async def test():
    return {"message": "HOME"}

@app.post("/Login")
async def Autenticador(credenciais: Loginrequest):
    if credenciais.usuario_id == 'admin' and credenciais.senha == "1234":
        token = criar_token({"sub": credenciais.usuario_id})
        return {"acess_token": token, "token_type":"bearer"}
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciais inválidas, verifique o ID e senha"
        )
