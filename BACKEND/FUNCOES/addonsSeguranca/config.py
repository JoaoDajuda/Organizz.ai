from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITH", "HS256")
ACESS_TOKEN_EXPIRE = int(os.getenv("ACCES_TOKEN_EXPIRE"))