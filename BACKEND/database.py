from sqlmodel import create_engine

# Mesma URL usada no alembic.ini (sqlalchemy.url).
# Se um dia mudar usuário/senha/host do banco, troque aqui E no alembic.ini.
DATABASE_URL = "mysql+pymysql://root:1234@localhost:3306/organizzai"

engine = create_engine(DATABASE_URL, echo=True)