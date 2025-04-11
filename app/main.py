from fastapi import FastAPI
from app.routers.book_router import router as book
from app.routers.basic_router import router as basic
from app.routers.auth_router import router as auth
from app.routers.user_router import router as user
from app.config.db import connect_to_db, close_db_connection

app = FastAPI(title="FastAPI CRUD Example")


async def lifespan():
    # Startup: Connect to the database
    await connect_to_db()
    yield  # FastAPI will wait here until the app shuts down
    # Shutdown: Close the database connection
    await close_db_connection()


app.include_router(book)
app.include_router(basic)
app.include_router(auth)
app.include_router(user)
