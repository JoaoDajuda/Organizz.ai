from fastapi import FastAPI
import os

app = FastAPI()

from auth_routes import auth_router
from math_routes import math_router, add_router, sub_router

app.include_router(auth_router)
app.include_router(math_router)
app.include_router(add_router)
app.include_router(sub_router)