from fastapi import HTTPException, status
from app.schemas.book_schema import Book, Genre, Language
from app.models import book_model
from fastapi.responses import JSONResponse
from app.utils import ErrorResponse, BaseResponse
from app.config.settings import settings
from app.config.db import connect_to_db


async def add_book(payload: Book, db):

    try:
        Language(payload.language)
        Genre(payload.genre)
        book_dict = payload.model_dump()
        print("db...", db)
        print("book_dict...", book_dict)
        print("book_dict...", type(book_dict))

        result = await db.books.insert_one(book_dict)
        print("result", result)
        created_id = str(result.inserted_id)
        # book_model.fake_books.append(payload)
        return {
            "status_code": status.HTTP_201_CREATED,
            "message": "Book created successfully",
            "data": created_id,
        }

    except ValueError as err:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Invalid enum value: {str(err)}",
        )


def get_books():
    try:
        print(settings.database_client)
        print(settings.database_name)
        books = book_model.fake_books
        return BaseResponse(
            message="Book fetched successfully",
            data=books,
            status_code=status.HTTP_200_OK,
        )

    except Exception as e:
        return ErrorResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message="Internal server error",
            error=str(e),
        )
