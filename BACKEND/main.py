from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise RuntimeError("SECRET_KEY não definida no .env")

ALGORITHM = os.getenv("ALGORITHM", "HS256")
TIMER = int(os.getenv("TIMER", "30"))  # minutos de validade do token

app = FastAPI()

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_schema = OAuth2PasswordBearer(tokenUrl="auth/login_form")

# Esses imports ficam DEPOIS das variáveis acima (evita import circular)
from auth_routes import auth_router
from math_routes import math_router
from act_routes import act_router

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(math_router)
app.include_router(act_router)