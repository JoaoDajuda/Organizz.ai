#!/usr/bin/env bash
set -Eeuo pipefail

ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
VENV="$ROOT/.venv"
LOG_DIR="$ROOT/.dev-logs"
WITH_OLLAMA=0
CHECK_ONLY=0
PIDS=()
SERVICE_NAMES=()

usage() {
    cat <<'EOF'
Uso:
    ./dev.sh                 Inicia backend, bot e web sem iniciar o Ollama
    ./dev.sh --with-ollama   Inicia também o Ollama e baixa llama3.2 se necessário
    ./dev.sh --check         Confere os pré-requisitos sem iniciar serviços
    ./dev.sh --help          Mostra esta ajuda
EOF
}

while (($#)); do
    case "$1" in
        --with-ollama) WITH_OLLAMA=1 ;;
        --check) CHECK_ONLY=1 ;;
        --help|-h) usage; exit 0 ;;
        *) printf 'Argumento desconhecido: %s\n\n' "$1" >&2; usage >&2; exit 2 ;;
    esac
    shift
done

require_command() {
    if ! command -v "$1" >/dev/null 2>&1; then
        printf 'Comando obrigatório não encontrado: %s\n' "$1" >&2
        exit 1
    fi
}

check_prerequisites() {
    require_command python3
    require_command node
    require_command npm
    require_command mysqladmin
    require_command sha256sum
    require_command setsid
    if ((WITH_OLLAMA)); then
        require_command ollama
    fi

    python3 -c 'import sys; sys.exit(0 if sys.version_info >= (3, 10) else 1)' || {
        printf 'Python 3.10 ou superior é necessário.\n' >&2
        exit 1
    }
    node -e 'const [major, minor] = process.versions.node.split(".").map(Number); process.exit(major > 20 || (major === 20 && minor >= 19) || major >= 22 ? 0 : 1)' || {
        printf 'Node.js 20.19+ ou 22.12+ é necessário para o Vite.\n' >&2
        exit 1
    }

    if [[ ! -f "$ROOT/BACKEND/.env" ]]; then
        printf 'Arquivo BACKEND/.env não encontrado.\n' >&2
        exit 1
    fi
    for key in SECRET_KEY ALGORITHM TIMER DATABASE_URL; do
        if [[ -z "${!key:-}" ]] && ! grep -Eq "^[[:space:]]*${key}[[:space:]]*=" "$ROOT/BACKEND/.env"; then
            printf 'A variável %s precisa estar definida no ambiente ou em BACKEND/.env.\n' "$key" >&2
            exit 1
        fi
    done

    if ! mysqladmin ping --silent >/dev/null 2>&1; then
        printf 'MySQL não está respondendo. Inicie o serviço MySQL e tente novamente.\n' >&2
        exit 1
    fi
}

check_prerequisites
if ((CHECK_ONLY)); then
    printf 'Pré-requisitos encontrados: Python, Node.js, npm, MySQL e configurações do BACKEND/.env.\n'
    if ((WITH_OLLAMA)); then
        printf 'Ollama instalado; será iniciado se ainda não estiver ativo.\n'
    else
        printf 'Ollama não será iniciado por este modo.\n'
    fi
    exit 0
fi

port_is_available() {
    python3 - "$1" <<'PY'
import socket
import sys

with socket.socket() as server:
    try:
        server.bind(("127.0.0.1", int(sys.argv[1])))
    except OSError:
        raise SystemExit(1)
PY
}

for port in 8000 8001 5173; do
    if ! port_is_available "$port"; then
        printf 'A porta %s já está em uso. Encerre o serviço que a ocupa e tente novamente.\n' "$port" >&2
        exit 1
    fi
done

mkdir -p "$LOG_DIR"

requirements_hash="$(cat "$ROOT/BACKEND/requirements.txt" "$ROOT/BOTS/requirements.txt" | sha256sum | cut -d ' ' -f 1)"
installed_requirements_hash="$(cat "$VENV/.requirements-hash" 2>/dev/null || true)"
if [[ ! -x "$VENV/bin/python" || "$installed_requirements_hash" != "$requirements_hash" ]]; then
    python3 -m venv "$VENV"
    "$VENV/bin/python" -m pip install --upgrade pip
    "$VENV/bin/python" -m pip install -r "$ROOT/BACKEND/requirements.txt" -r "$ROOT/BOTS/requirements.txt"
    printf '%s\n' "$requirements_hash" > "$VENV/.requirements-hash"
fi

if ! (
    cd "$ROOT/BACKEND"
    "$VENV/bin/python" - <<'PY'
from database import engine

with engine.connect():
    pass
PY
) >"$LOG_DIR/database-check.log" 2>&1; then
    printf 'Não foi possível autenticar no MySQL com DATABASE_URL. Confira BACKEND/.env e veja .dev-logs/database-check.log.\n' >&2
    exit 1
fi

web_package_hash="$(sha256sum "$ROOT/FRONTEND/web/package.json" | cut -d ' ' -f 1)"
installed_web_hash="$(cat "$ROOT/FRONTEND/web/node_modules/.organizzai-package-hash" 2>/dev/null || true)"
if [[ ! -x "$ROOT/FRONTEND/web/node_modules/.bin/vite" || "$installed_web_hash" != "$web_package_hash" ]]; then
    (
        cd "$ROOT/FRONTEND/web"
        npm install --package-lock=false --workspaces=false
        printf '%s\n' "$web_package_hash" > node_modules/.organizzai-package-hash
    )
fi

printf 'Aplicando migrations do banco...\n'
(
    cd "$ROOT/BACKEND"
    "$VENV/bin/alembic" upgrade head
)

start_service() {
    local name="$1"
    local workdir="$2"
    shift 2
    (
        cd "$workdir"
        exec setsid "$@"
    ) >"$LOG_DIR/$name.log" 2>&1 &
    local pid="$!"
    PIDS+=("$pid")
    SERVICE_NAMES+=("$name")
    printf '%s iniciado (PID %s); log: .dev-logs/%s.log\n' "$name" "$pid" "$name"
}

cleanup() {
    local exit_code=$?
    trap - EXIT INT TERM
    for pid in "${PIDS[@]}"; do
        kill -TERM -- "-$pid" 2>/dev/null || kill -TERM "$pid" 2>/dev/null || true
    done
    for pid in "${PIDS[@]}"; do
        wait "$pid" 2>/dev/null || true
    done
    exit "$exit_code"
}

trap cleanup EXIT
trap 'exit 130' INT
trap 'exit 143' TERM

ollama_is_running() {
    "$VENV/bin/python" - <<'PY' >/dev/null 2>&1
from urllib.request import urlopen

with urlopen("http://127.0.0.1:11434/api/tags", timeout=1):
    pass
PY
}

if ((WITH_OLLAMA)); then
    if ! ollama_is_running; then
        start_service ollama "$ROOT" ollama serve
        printf 'Aguardando o Ollama iniciar...\n'
        if ! "$VENV/bin/python" - <<'PY'
import time
from urllib.error import URLError
from urllib.request import urlopen

for _ in range(60):
    try:
        with urlopen("http://127.0.0.1:11434/api/tags", timeout=1):
            break
    except (OSError, URLError):
        time.sleep(0.5)
else:
    raise SystemExit("Ollama não iniciou. Consulte .dev-logs/ollama.log.")
PY
        then
            exit 1
        fi
    fi

    if ! ollama list | awk 'NR > 1 { print $1 }' | grep -Eq '^llama3\.2(:latest)?$'; then
        ollama pull llama3.2
    fi
fi

start_service backend "$ROOT/BACKEND" "$VENV/bin/uvicorn" main:app --reload --port 8000
start_service bot "$ROOT/BOTS" "$VENV/bin/uvicorn" main:app --reload --port 8001
start_service web "$ROOT/FRONTEND/web" npm run dev -- --host 0.0.0.0

printf '\nProjeto iniciado:\n  Web:     http://localhost:5173\n  Backend: http://localhost:8000\n  Bot WS:  ws://localhost:8001/robo/ws\n'
if ((WITH_OLLAMA)); then
    printf '  Ollama:  http://localhost:11434 (llama3.2)\n'
else
    printf '  Ollama:  não iniciado por este comando\n'
fi
printf '\nPressione Ctrl+C para encerrar os serviços iniciados por este script.\n'

set +e
wait -n "${PIDS[@]}"
exit_code=$?
set -e
printf 'Um serviço encerrou (código %s); finalizando os demais.\n' "$exit_code" >&2
exit "$exit_code"