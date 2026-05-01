from datetime import datetime, date
import os
import json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

ARQUIVO = os.path.abspath(os.path.join(BASE_DIR, "..", "JSONs", "tarefas.json"))

def carregar_dados():
    if not os.path.exists(ARQUIVO):
        return {}
    with open(ARQUIVO, "r", encoding='utf-8') as f:
        return json.load(f)

def salvar_dados(tarefas):
    os.makedirs(os.path.dirname(ARQUIVO), exist_ok=True)
    with open(ARQUIVO, "w", encoding='utf-8') as f:
        json.dump(tarefas, f, indent=4, ensure_ascii=False)

def Definirtarefa():
    print("\n--- Cadastro de Nova Tarefa ---")
    print("Digite o título da tarefa")
    nome = input(">> ").strip()

    if not nome:
        print("O título não pode ser vazio!")
        return

    print("Digite a data da tarefa com dia/mês/ano (ex: 12/04/2026)")
    datatarefa = input(">> ").strip()

    try:
        datatraduz = datetime.strptime(datatarefa, "%d/%m/%Y")
        
        hoje = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

        if datatraduz < hoje:
            print("Erro: Não é possível agendar tarefas para datas passadas!")
            return
        
        datastring = datatraduz.strftime('%d de %B de %Y')

        tarefas = carregar_dados()

        contador = 1
        nometarefa = "Tarefa"
        while nometarefa in tarefas:
            nometarefa = f"Tarefa{contador}"
            contador += 1

        tarefas[nometarefa] = {
            "Titulo": nome,
            "Data": datastring
        }

        salvar_dados(tarefas)
        print(f"Definido compromisso para {datastring}")

    except ValueError:
        print("Erro: Formato de data inválido! Use DD/MM/AAAA.")

if __name__ == "__main__":
   
    while True:
        Definirtarefa()
        print("\n" + "-"*30)
        continuar = input("Deseja adicionar outra tarefa? (s/n): ").lower()
        if continuar != 's':
            print("Encerrando... Não esqueça de rodar o main.py para atualizar o banco!")
            break