# Variável global para o saldo
saldo = 0
# LISTA ADICIONADA: Para capturar cada movimentação individual
historico = [] 

def versaldo():
    global saldo
    print("- - - - - - - - - - - - - -")
    print(f"Seu saldo é de: {saldo}")
    print("- - - - - - - - - - - - - -")