import json
import os

BASE_DIR = os.path.dirname(__file__)
ARQUIVO = os.path.join(BASE_DIR, "JSONs", "dados.json")

# Criar arquivo se não existir
def iniciar_dados():
    if not os.path.exists(ARQUIVO):
        dados = {
            "saldo": 0,
            "entradas": [],
            "saidas": []
        }
        salvar_dados(dados)

def carregar_dados():
    with open(ARQUIVO, "r") as f:
        return json.load(f)

def salvar_dados(dados):
    with open(ARQUIVO, "w") as f:
        json.dump(dados, f, indent=4)


def subvalor():
    print()
    while True:
        add = int(input())
        if add == 999:
            break
        elif add == 998:
            return
        
        dados = carregar_dados()
        dados["saldo"] -= add
        dados["saidas"].append(add)

        salvar_dados(dados)

        print("- - - - - - - - - - - - - -")
        print(dados["saldo"])
        print("- - - - - - - - - - - - - -")


def addvalor():
    print()
    while True:
        add = int(input())
        if add == 999:
            break
        elif add == 998:
            return
        
        dados = carregar_dados()
        dados["saldo"] += add
        dados["entradas"].append(add)

        salvar_dados(dados)

        print("- - - - - - - - - - - - - -")
        print(dados["saldo"])
        print("- - - - - - - - - - - - - -")


def versaldo():
    dados = carregar_dados()
    print("- - - - - - - - - - - - - -")
    print("Seu saldo é de:")
    print(dados["saldo"])
    print("- - - - - - - - - - - - - -")


def main():
    iniciar_dados()
    

while True:
        print(f'Digite o que deseja realizar:')
        print(f'1 - Adicionar saldo')
        print(f'2 - Subtrair compra')

        print(f'3 - ver saldo') 
        print('=-=-=-=-=-=-=-')
        choose = (' ')
        choose = input('digite uma opção: ')
        
        if choose == '1':
            addvalor()
        elif choose == '2':
            subvalor()
        elif choose == '3' or choose == 'ver':
            versaldo()
        else:
            print('=-=-==-=-=-=')
            print('formato inválido, digite novamente')
            print('=-=-=-==-=-')            

def addvalor() : 
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
                global saldo 
                saldo += add_value
                print("- - - - - - - - - - - - - -")
                print ('valor adicionado');
                print("- - - - - - - - - - - - - -")

            except:
                print('opção inválida, digite um valor válida')

def subvalor() : 
    while True:
        print('Digite um valor para subtrair(sair ou voltar): ')
        add = input()
        if add == 'sair':
            print('saindo...')
            break
        elif add == 'voltar':
            return 
        else:
            try:
                add_value = int(add)
                global saldo 
                saldo -= add_value
                print("- - - - - - - - - - - - - -")
                print ('valor subtraido');
                print("- - - - - - - - - - - - - -")
            except:  
                print('opção inválida, digite um valor válida')

       
def versaldo():
    global saldo
    print("- - - - - - - - - - - - - -")
    print(f"Seu saldo é de: {saldo}")
    print("- - - - - - - - - - - - - -")
    

def Funcionapf() :
    main()
    
Funcionapf()
        


