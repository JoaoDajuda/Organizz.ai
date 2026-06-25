from fastapi import FastAPI

from ..ORCAMENTO.subtracao import subvalor

from ..ORCAMENTO.soma import addvalor

app = FastAPI()

# rota para somar valores e enviar ao banco
@app.get("/soma/{valor}")
async def somar(valor: float):
    resultado = addvalor(valor)
    return resultado


# rota para subtrair valores e enviar ao banco
@app.get("/subtracao/{valor}")
async def subtrair(valor: float):
    resultado = subvalor(valor)
    return resultado

@app.get("/saldo")
async def versaldo(id: int, senha: str):
    saldo = versaldo(id, senha)
    return saldo

@app.get("/")
async def root():
    return {"message": "JJPZ"}