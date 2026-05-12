from datetime import datetime

# Memória temporária para as tarefas
tarefas_memoria = {}

def Definirtarefa():
    global tarefas_memoria
    print("\n--- Cadastro de Nova Tarefa ---")
    print("Digite o título da tarefa")
    nome = input(">> ").strip()

    if not nome:
        print("O título não pode ser vazio!")
        return

    print("Digite a data (ex: 12/04/2026)")
    datatarefa = input(">> ").strip()

    try:
        datatraduz = datetime.strptime(datatarefa, "%d/%m/%Y")
        hoje = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

        if datatraduz < hoje:
            print("Erro: Não é possível agendar para o passado!")
            return
        
        datastring = datatraduz.strftime('%d de %B de %Y')

        contador = 1
        nometarefa = "Tarefa"
        while nometarefa in tarefas_memoria:
            nometarefa = f"Tarefa{contador}"
            contador += 1

        tarefas_memoria[nometarefa] = {"Titulo": nome, "Data": datastring}
        print(f"Definido compromisso para {datastring}")

    except ValueError:
        print("Erro: Formato de data inválido!")

def abrir_agenda():
    while True:
        print("\n==== MENU AGENDA ====")
        print("1 - Cadastrar Nova Tarefa")
        print("0 - Voltar ao Menu Principal")
        print("======================")
        
        opcao = input(">> ")
        if opcao == "1":
            Definirtarefa()
        elif opcao == "0":
            break
        else:
            print("Opção inválida.")