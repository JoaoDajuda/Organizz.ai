from fastapi import FastAPI
import os

app = FastAPI()

from auth_routes import auth_router
from math_routes import math_router

app.include_router(auth_router)
app.include_router(math_router)


# from fastapi.middleware.cors import CORSMiddleware

# app.add.middleware(
#     CORSMiddleware,
#     allow_origins=["https://localhost:5173"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     )