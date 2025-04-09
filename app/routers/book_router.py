from fastapi import APIRouter
from app.controller.book_controller import add_book, get_books
from app.schemas.book_schema import Book

router = APIRouter(prefix="/book", tags=["book"])


@router.post("/add", response_model=Book)
def create(book: Book):
    return add_book(book)


@router.get("/", response_model=list[Book])
def getAll():
    return get_books()
