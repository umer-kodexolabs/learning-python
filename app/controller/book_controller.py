from fastapi import HTTPException, status
from app.schemas.book_schema import Book, Genre, Language
from app.models import book_model
import json
from fastapi.responses import JSONResponse


def add_book(payload: Book):
    try:
        Language(payload.language)
        Genre(payload.genre)
        book_model.fake_books.append(payload)
        return {
            "status_code": status.HTTP_201_CREATED,
            "message": "Book created successfully",
            "data": payload,
        }

    except ValueError as err:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Invalid enum value: {str(err)}",
        )


def get_books():
    print("I am here")
    books = book_model.fake_books
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "status_code": status.HTTP_200_OK,
            "message": "Book fetched successfully",
            "data": books,
        },
    )
