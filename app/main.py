from fastapi import FastAPI
# from .routes1 import router
from app.routers.book_router import router as book

app = FastAPI(title="FastAPI CRUD Example")

# app.include_router(router)
app.include_router(book)