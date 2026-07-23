from fastapi import FastAPI
from pydantic import BaseModel, Field

from ..FUNCOES_ORCAMENTO.orcamento import addvalor_v2, subvalor_v2,versaldo,Autenticar

from ..ORCAMENTO.soma import addvalor

from .registerRoute import Loginrequest, Autenticar

app = FastAPI()


@app.get("/soma/{valor}")
async def somar(valor: float):
    """ 
    rota para somar valores e enviar ao banco
    """
    resultado = addvalor_v2(valor)
    return resultado

@app.get("/subtracao/{valor}")
async def subtrair(valor: float):
    """
    rota para subtrair valores e enviar ao banco
    """
    resultado = subvalor_v2(valor)
    return resultado

@app.get("/saldo")
async def versaldo(id: int, senha: str):
    """
    visualizar saldo
    """
    saldo = versaldo(id, senha)
    return saldo

@app.get("/")
async def test():
    return {"message": "HOME"}

@app.post("validador")
async def Autenticador(credenciais: Loginrequest):
    """validador provisório(será substtituido em breve)"""
    resultado = await Autenticar(credenciais)
    return resultado