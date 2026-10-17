# Execução local do Organizz.ai

Requisitos locais: Python 3.10+, Node.js 20.19+ ou 22.12+, npm, MySQL instalado e iniciado, e `BACKEND/.env` configurado com `SECRET_KEY`, `ALGORITHM`, `TIMER` e `DATABASE_URL`. Consulte [BACKEND/.env.example](BACKEND/.env.example) para os nomes e formatos, sem copiar os valores de exemplo como credenciais reais. O script não instala nem inicia o MySQL.

Se aparecer `Access denied for user 'root'@'localhost'` (erro 1698), o MySQL provavelmente está configurado para autenticar `root` pelo socket do sistema. Crie um usuário da aplicação pelo cliente administrativo do MySQL e configure a URL desse usuário em `BACKEND/.env`:

```sql
CREATE DATABASE IF NOT EXISTS organizzai;
CREATE USER 'organizzai_app'@'localhost' IDENTIFIED BY 'escolha-uma-senha';
GRANT ALL PRIVILEGES ON organizzai.* TO 'organizzai_app'@'localhost';
FLUSH PRIVILEGES;
```

Use `DATABASE_URL=mysql+pymysql://organizzai_app:SENHA_URL_ENCODED@localhost:3306/organizzai`. Se a senha tiver caracteres reservados de URL, codifique-os (por exemplo, `@` como `%40`). Não coloque a senha no script ou no repositório.

Na raiz do repositório, execute:

```sh
./dev.sh
```

Esse modo instala as dependências necessárias na primeira execução, aplica as migrations e inicia backend, bot e frontend. Ele não inicia o Ollama; o chat só gera respostas se um Ollama já estiver acessível em `http://localhost:11434`.

Para também iniciar o Ollama e baixar `llama3.2` se ainda não estiver instalado:

```sh
./dev.sh --with-ollama
```

O Ollama iniciado pelo script é encerrado com os outros serviços ao pressionar Ctrl+C. Se já houver uma instância do Ollama ativa, o script a reutiliza e não a encerra.

Para conferir pré-requisitos sem iniciar a aplicação, use `./dev.sh --check`. Os logs ficam em `.dev-logs/`; o script encerra os serviços que ele próprio iniciou quando recebe Ctrl+C.