from .valor import *
def subvalor(valor):
    try:
        #subtrair o valor passado em body no banco
        sub_valor = float(valor)
        if sub_valor < 0:
            raise ValueError("O valor subtraído não pode ser negativo.")
        dados["saldo"] -= sub_valor
        return ({"message": f"Valor {sub_valor} subtraído."})
        return (sub_valor)
    except:
        return ({"message": "Erro na função subtrair valor."})