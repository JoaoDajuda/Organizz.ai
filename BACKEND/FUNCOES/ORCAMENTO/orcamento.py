# Variável global para o saldo
saldo = 0
# LISTA ADICIONADA: Para capturar cada movimentação individual
historico = [] 

def addvalor_v2(): 
    global saldo, historico # Adicionado historico no global
    print()
    while True:
        add = str(input('digite um valor para acrescentar(sair ou voltar): '))   
        if add == 'sair':
            break
        elif add == 'voltar':
            return  
        else:
            try:
                add_value = int(add)
                saldo += add_value
                # ANOTAÇÃO: Salva o valor positivo na lista
                historico.append(add_value) 
                
                print("- - - - - - - - - - - - - -")
                print('valor adicionado')
                print("- - - - - - - - - - - - - -")
            except:
                print('opção inválida, digite um valor válido')

def subvalor_v2(): 
    global saldo, historico # Adicionado historico no global
    while True:
        print('Digite um valor para subtrair(sair ou voltar): ')
        add = input()
        if add == 'sair':
            break
        elif add == 'voltar':
            return 
        else:
            try:
                add_value = int(add)
                saldo -= add_value
                # ANOTAÇÃO: Salva o valor negativo na lista para o banco saber que é saída
                historico.append(-add_value) 
                
                print("- - - - - - - - - - - - - -")
                print('valor subtraído')
                print("- - - - - - - - - - - - - -")
            except:  
                print('opção inválida, digite um valor válido')

def versaldo():
    global saldo
    print("- - - - - - - - - - - - - -")
    print(f"Seu saldo é de: {saldo}")
    print("- - - - - - - - - - - - - -")

def abrir_orcamento():
    while True:
        print(f'\n--- MENU ORÇAMENTO ---')
        print(f'1 - Adicionar saldo')
        print(f'2 - Subtrair compra')
        print(f'3 - Ver saldo') 
        print('0 - Voltar ao Menu Principal')
        print('----------------------')
        choose = input('digite uma opção: ')
        
        if choose == '1':
            addvalor_v2()
        elif choose == '2':
            subvalor_v2()
        elif choose == '3' or choose == 'ver':
            versaldo()
        elif choose == '0':
            break
        else:
            print('Formato inválido, tente novamente.')