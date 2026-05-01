from ORCAMENTO.valor import *
def subvalor() : 
    while True:
        add = input('Digite um valor para subtrair("voltar" para retroceder): ').lower
        if add == 'voltar':
            return 
        
        else:
            try:
                add_value = float(add)
                if dados['saldo'] < add_value:
                    print('saldo insuficiente')

                elif add_value <= 0:
                    print('não é possivel somar zero, tente novamente')
                else:
                    dados["saldo"] -= add_value
                    print("- - - - - - - - - - - - - -")
                    print (f'valor {add}R$ subtraido')
                    print("- - - - - - - - - - - - - -")
            except:  
                print('opção inválida, digite um valor válida')