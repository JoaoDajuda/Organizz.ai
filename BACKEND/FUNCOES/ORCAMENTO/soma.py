from .valor import *

def addvalor(valor):
    try:
        #somar o valor passado em body no banco
        add_valor = float(valor)
        if add_valor < 0:
            raise ValueError("O valor adicionado não pode ser negativo.")
        dados["saldo"] += add_valor
        return ({"message": f"Valor {add_valor} adicionado."})
        return (add_valor)
    except:
        return ({"message": "Erro na função adicionar valor."})