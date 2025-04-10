from fastapi import APIRouter, Depends
from app.controllers.book_controller import add_book, get_books
from app.schemas.book_schema import Book
from app.utils import BaseResponse
from motor.motor_asyncio import AsyncIOMotorClient
from app.config.db import connect_to_db

router = APIRouter(prefix="/book", tags=["book"])


@router.post("/add", response_model=BaseResponse)
async def create(book: Book, db: AsyncIOMotorClient = Depends(connect_to_db)):
    return await add_book(book, db)


@router.get("/", response_model=BaseResponse)
def getAll():
    return get_books()
