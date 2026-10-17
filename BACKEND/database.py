import os
from pathlib import Path

from dotenv import load_dotenv
from sqlmodel import create_engine

load_dotenv(Path(__file__).with_name(".env"))

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
	raise RuntimeError("Defina DATABASE_URL em BACKEND/.env para conectar ao MySQL.")

engine = create_engine(DATABASE_URL, echo=True)