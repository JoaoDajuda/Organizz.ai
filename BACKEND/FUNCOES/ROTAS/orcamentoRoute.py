from fastapi import FastAPI
from pydantic import BaseModel, Field

from ..FUNCOES_ORCAMENTO.orcamento import addvalor_v2, subvalor_v2,versaldo,Autenticar

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
    resultado = await Autenticar(credenciais)
    return resultado