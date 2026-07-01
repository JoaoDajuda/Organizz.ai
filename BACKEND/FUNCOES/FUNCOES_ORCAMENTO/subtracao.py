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