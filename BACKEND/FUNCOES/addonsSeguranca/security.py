
def criar_token(dados: dict, expira_em: timedelta = None):
    #cria um jwt assinado contendo os dados informados:
    codificador = dados.copy()

    if expira_em:
        ex