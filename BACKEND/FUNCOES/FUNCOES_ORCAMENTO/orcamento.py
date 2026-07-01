from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field

# Variável global para o saldo
saldo = 0
# LISTA ADICIONADA: Para capturar cada movimentação individual
historico = [] 
login = False

def validacao(login):
    if login == True:
        print('fé')

    else:
        print("Faça login para continuar")
        Autenticar()
def addvalor_v2(): 
    global saldo, historico # Adicionado historico no global
    print()
    if login == True:
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

#modelo do body
class Loginrequest(BaseModel):
    usuario_id: str = Field(...,min_length=3, description="ID do Usuário")
    senha: str=Field(...,min_length=3, description="Senha do Usuário")


async def Autenticar(credenciais: Loginrequest):
    #validando dados
    if credenciais.usuario_id == "admin" and credenciais.senha == "1234":
        login = True
        return{"status": "sucesso",}       
    
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas. Verifique o ID e a senha."
        )