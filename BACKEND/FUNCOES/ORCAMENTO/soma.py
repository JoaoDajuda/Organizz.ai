from funcoes.valor import *

def addvalor() :
    
    print()
    while True:
        add = input('digite um valor para acrescentar("voltar" para retroceder): ')
        if add == 'voltar':
            return 
        else:
            try:
                add_value = float(add)
                if add_value <= 0:
                    print('digite um valor válido')

                else:
                    dados["saldo"] += add_value
                    print("- - - - - - - - - - - - - -")
                    print (f'valor {add}R$ adicionado')
                    print("- - - - - - - - - - - - - -")

            except:
                print('opção inválida ou inexistente, digite um valor válido')
