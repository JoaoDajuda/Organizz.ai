import os
from pathlib import Path

from dotenv import load_dotenv
from sqlmodel import create_engine

load_dotenv(Path(__file__).with_name(".env"))

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
	raise RuntimeError("Defina DATABASE_URL em BACKEND/.env para conectar ao MySQL.")

engine = create_engine(DATABASE_URL, echo=True)

from sqlmodel import create_engine

# Mesma URL usada no alembic.ini (sqlalchemy.url).
# Se um dia mudar usuário/senha/host do banco, troque aqui E no alembic.ini.
DATABASE_URL = "mysql+pymysql://organizz_app@127.0.0.1:3306/organizz_ai"

engine = create_engine(DATABASE_URL, echo=True)