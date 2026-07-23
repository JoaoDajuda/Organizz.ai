from fastapi import FastAPI
import os

app = FastAPI()

from auth_routes import auth_router

app.include_router(auth_router)
