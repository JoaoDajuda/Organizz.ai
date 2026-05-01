# Definiremos o FASTapi
from fastapi import FastAPI
from orcamento import main
from orcamento import versaldo


app = FastAPI()
@app.get('/ver-saldo')
async def rota_saldo():
    valor = versaldo()
    return {valor}