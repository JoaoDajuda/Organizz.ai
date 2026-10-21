from sqlmodel import create_engine

# Mesma URL usada no alembic.ini (sqlalchemy.url).
# Se um dia mudar usuário/senha/host do banco, troque aqui E no alembic.ini.
DATABASE_URL = "mysql+pymysql://dbeaver_user:BewareTheWater@127.0.0.1:3306/organizz_ai"

engine = create_engine(DATABASE_URL, echo=True)