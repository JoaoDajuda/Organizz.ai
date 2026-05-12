from ORCAMENTO import orcamento
from AGENDA import agendas

def menu_principal(salvar_fn):
    while True:
        print("\n============================")
        print("      ORGANIZZ.AI      ")
        print("============================")
        print("1 - Ir para Orçamento")
        print("2 - Ir para Agenda")
        print("0 - Fechar Programa")
        print("----------------------------")
        
        opcao = input("Selecione para onde deseja ir: ")

        if opcao == "1":
            orcamento.abrir_orcamento()
            salvar_fn("financeiro") 
        elif opcao == "2":
            agendas.abrir_agenda()
            salvar_fn("agenda")    
        elif opcao == "0":
            print("Finalizando sistema...")
            break
        else:
            print("Opção incorreta.")