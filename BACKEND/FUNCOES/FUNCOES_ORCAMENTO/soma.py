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
    else:
        print('Login não encontrado')