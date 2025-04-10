from fastapi import APIRouter, Depends
from app.controllers.book_controller import (
    add_book,
    get_books,
    get_book,
    delete_book,
    update_book,
    test_function,
)
from fastapi import Request
from app.schemas.book_schema import Book, UpdateBook
from motor.motor_asyncio import AsyncIOMotorClient
from app.config.db import connect_to_db

router = APIRouter(prefix="/book", tags=["book"])


@router.get("/test")
def test_query(
    req: Request,
    limit: int = None,
    page: int = None,
    is_new: bool = False,
):
    p = {limit, page}
    print("Python", type(p))
    return test_function(limit, page, is_new, req)


@router.post("/")
async def create(book: Book, db: AsyncIOMotorClient = Depends(connect_to_db)):
    return await add_book(
        book,
        db,
    )


@router.get("/")
async def get_all(db: AsyncIOMotorClient = Depends(connect_to_db)):
    return await get_books(db)


@router.get("/{book_id}")
async def get_by_id(book_id: str, db: AsyncIOMotorClient = Depends(connect_to_db)):
    return await get_book(book_id, db)


@router.delete("/{book_id}")
async def delete_book_by_id(
    book_id: str, db: AsyncIOMotorClient = Depends(connect_to_db)
):
    return await delete_book(book_id, db)


@router.patch("/{book_id}")
async def update_book_by_id(
    book_id: str, book: UpdateBook, db: AsyncIOMotorClient = Depends(connect_to_db)
):
    return await update_book(
        book_id,
        book,
        db,
    )
