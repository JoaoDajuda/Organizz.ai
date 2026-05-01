import sqlite3
import json
import os
import time
from datetime import datetime

# --- CONFIGURAÇÃO DE CAMINHOS ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Caminho para a pasta JSONs que está no mesmo nível da pasta back-end
JSON_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", "JSONs"))
DADOS_PATH = os.path.join(JSON_DIR, "JSONs/dados.json")
TAREFAS_PATH = os.path.join(JSON_DIR, "JSONs/tarefas.json")
# Caminho para o banco de dados
DB_PATH = os.path.join(BASE_DIR, "database", "banco.db")

def iniciar_banco():
    """Cria as tabelas conforme o diagrama ER do TCC."""
    if not os.path.exists(os.path.dirname(DB_PATH)):
        os.makedirs(os.path.dirname(DB_PATH))
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Usuario (id, nome, senha, email)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Usuario (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            senha TEXT,
            email TEXT UNIQUE
        )
    """)
    
    # RTreino (id, dia_treino, repeticoes, grupo_muscular, exercicio, N_Series)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS RTreino (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            dia_treino TEXT,
            repeticoes INTEGER,
            grupo_muscular TEXT,
            exercicio TEXT,
            N_Series INTEGER
        )
    """)
    
    # Agenda (id, tarefa, data)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Agenda (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tarefa TEXT,
            data TEXT
        )
    """)
    
    # Financeiro (id, Saldo)
    cursor.execute("CREATE TABLE IF NOT EXISTS Financeiro (id INTEGER PRIMARY KEY, Saldo FLOAT)")
    
    # Transacoes (id, tipo, valor) - O extrato detalhado
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Transacoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tipo TEXT,
            valor FLOAT
        )
    """)
    
    conn.commit()
    return conn, cursor

def sincronizar():
    """Lê os arquivos JSON, valida os dados e atualiza o Banco de Dados."""
    if not os.path.exists(DADOS_PATH) or not os.path.exists(TAREFAS_PATH):
        print(f"⚠️ [{time.strftime('%H:%M:%S')}] Aguardando criação dos arquivos JSON...")
        return

    conn, cursor = iniciar_banco()

    try:
        # --- 1. SINCRONIZAR FINANCEIRO E TRANSAÇÕES ---
        with open(DADOS_PATH, 'r', encoding='utf-8') as f:
            dados_fin = json.load(f)
        
        # Atualiza Saldo Geral
        cursor.execute("INSERT OR REPLACE INTO Financeiro (id, Saldo) VALUES (1, ?)", (dados_fin.get('saldo', 0),))

        # Atualiza Transações (Entradas e Saídas)
        cursor.execute("DELETE FROM Transacoes")
        cursor.execute("DELETE FROM sqlite_sequence WHERE name='Transacoes'")
        
        for v in dados_fin.get('entradas', []):
            cursor.execute("INSERT INTO Transacoes (tipo, valor) VALUES ('entrada', ?)", (v,))
        for v in dados_fin.get('saidas', []):
            cursor.execute("INSERT INTO Transacoes (tipo, valor) VALUES ('saida', ?)", (v,))

        # --- 2. SINCRONIZAR AGENDA (Com filtro de data) ---
        with open(TAREFAS_PATH, 'r', encoding='utf-8') as f:
            tarefas_json = json.load(f)

        cursor.execute("DELETE FROM Agenda")
        cursor.execute("DELETE FROM sqlite_sequence WHERE name='Agenda'")
        
        hoje = datetime.now().date()

        for info in tarefas_json.values():
            titulo = info.get('Titulo')
            data_str = info.get('Data') # Ex: "25 de April de 2026"
            
            try:
                # Converte a string do JSON de volta para data para conferir se já passou
                # Usamos %B porque seu agendas.py salva o nome do mês por extenso
                data_objeto = datetime.strptime(data_str, "%d de %B de %Y").date()
                
                if data_objeto >= hoje:
                    cursor.execute("INSERT INTO Agenda (tarefa, data) VALUES (?, ?)", (titulo, data_str))
            except:
                # Se a data estiver em formato estranho ou antigo, ignoramos para não quebrar o banco
                continue

        conn.commit()
        print(f"✅ [{time.strftime('%H:%M:%S')}] Banco Sincronizado e Datas Organizadas!")

    except Exception as e:
        print(f"❌ Erro na sincronização: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    print("🚀 SERVIÇO DE SINCRONIZAÇÃO INICIADO")
    print("Monitorando alterações em 'dados.json' e 'tarefas.json'...")
    print("Pressione CTRL + C para encerrar.")
    print("-" * 50)
    
    try:
        while True:
            sincronizar()
            time.sleep(5) # Atualiza a cada 5 segundos
    except KeyboardInterrupt:
        print("\n👋 Serviço de sincronização encerrado.")