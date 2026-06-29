import sqlite3
import menu
# Como o main.py já está dentro de FUNCOES, importamos direto as pastas filhas
from FUNCOES_ORCAMENTO import orcamento
from AGENDA import agendas

# Conecta ao banco de dados (o arquivo será criado na pasta FUNCOES)
conexao = sqlite3.connect('OrganizzAi.db')
cursor = conexao.cursor()

sql_script = """
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS Usuario (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    senha TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS Agenda (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_usuario INTEGER NOT NULL,
    tarefa_titulo TEXT NOT NULL,
    data_texto TEXT,
    status TEXT CHECK(status IN ('pendente', 'concluido', 'em_andamento')),
    FOREIGN KEY (id_usuario) REFERENCES Usuario(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Financeiro (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_usuario INTEGER NOT NULL UNIQUE,
    saldo REAL NOT NULL,
    FOREIGN KEY (id_usuario) REFERENCES Usuario(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Transacoes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_usuario INTEGER NOT NULL,
    tipo TEXT CHECK(tipo IN ('entrada', 'saida')),
    valor REAL NOT NULL,
    data_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_usuario) REFERENCES Usuario(id) ON DELETE CASCADE
);

INSERT OR IGNORE INTO Usuario (id, nome, senha, email) 
VALUES (1, 'Teste', '1234', 'teste@gmail.com');

INSERT OR IGNORE INTO Financeiro (id_usuario, saldo) VALUES (1, 0.0);
"""

def salvar_no_banco(tipo_operacao):
    try:
        if tipo_operacao == "financeiro":
            # Salva o saldo total atualizado
            cursor.execute("UPDATE Financeiro SET saldo = ? WHERE id_usuario = ?", (orcamento.saldo, 1))
            
            # Registra cada item do histórico como uma transação nova
            for valor in orcamento.historico:
                tipo_mov = "entrada" if valor > 0 else "saida"
                cursor.execute("INSERT INTO Transacoes (id_usuario, tipo, valor) VALUES (?, ?, ?)", 
                               (1, tipo_mov, abs(valor)))
                print(f"-> [BANCO] Registrada {tipo_mov} de {abs(valor)}")
            #add commit
            # Limpa o histórico para não duplicar na próxima vez que abrir o menu
            orcamento.historico.clear()
            
        elif tipo_operacao == "agenda":
            # ... (mantenha sua lógica da agenda igual)
            if agendas.tarefas_memoria:
                ultima_chave = list(agendas.tarefas_memoria.keys())[-1]
                tarefa = agendas.tarefas_memoria[ultima_chave]
                cursor.execute("INSERT INTO Agenda (id_usuario, tarefa_titulo, data_texto, status) VALUES (?, ?, ?, ?)", 
                               (1, tarefa["Titulo"], tarefa["Data"], "pendente"))
                agendas.tarefas_memoria.clear() 

        conexao.commit()
        
    except Exception as e:
        print(f"-> [ERRO SQLITE] {e}")    # AQUI NÃO VAI FINALLY COM CLOSE!

# --- O CORAÇÃO DO PROGRAMA ---
try:
    cursor.executescript(sql_script)
    conexao.commit()
    print("Banco de dados pronto!")
    
    # O menu roda aqui dentro. Ele só sai daqui quando você digita '0' no menu principal
    menu.menu_principal(salvar_no_banco)

except Exception as e:
    print(f"Erro fatal: {e}")

finally:
    # ESTE é o único finally que deve ter o close.
    # Ele só roda quando o menu_principal termina (quando o usuário fecha o programa)
    conexao.close()
    print("Conexão encerrada. Até logo!")