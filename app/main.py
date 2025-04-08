from fastapi import FastAPI
from .routes import router

app = FastAPI(title="FastAPI CRUD Example")

app.include_router(router)
