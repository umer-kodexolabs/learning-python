from fastapi import HTTPException, status, Response, Request
from app.schemas.book_schema import Book, Genre, Language
from app.models import book_model
from fastapi.responses import JSONResponse
from app.utils import success_response, error_response
from app.config.settings import settings
from app.config.db import connect_to_db
from fastapi.encoders import jsonable_encoder
from app.utils import convert_to_serializable
from datetime import datetime, timezone
from bson import ObjectId


async def add_book(
    payload: Book,
    db,
):

    try:
        Language(payload.language)
        Genre(payload.genre)
        book_dict = payload.model_dump()
        book_dict.update(
            {
                "isActive": True,
                "createdAt": datetime.now(timezone.utc),
                "updatedAt": datetime.now(timezone.utc),
            }
        )

        result = await db.books.insert_one(book_dict)

        created_id = str(result.inserted_id)

        return success_response(
            message="Book created successfully",
            status_code=status.HTTP_201_CREATED,
            data=created_id,
        )

    except ValueError as err:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Invalid enum value: {str(err)}",
        )


async def get_books(db):
    try:
        books = await db.books.find().to_list()
        json_books = convert_to_serializable(books)
        print(json_books)
        return success_response(
            message="Books fetched successfully",
            data=json_books,
            status_code=status.HTTP_200_OK,
        )

    except Exception as err:
        return error_response(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message="Internal server error2123",
            error=str(err),
        )


async def get_book(book_id, db):
    try:
        book = await db.books.find_one({"_id": ObjectId(book_id)})

        if book is None:
            return error_response(
                status_code=status.HTTP_404_NOT_FOUND,
                message="Book not found",
                error="Book not found",
            )

        data = convert_to_serializable(book)

        return success_response(
            message="Books fetched successfully",
            data=data,
            status_code=status.HTTP_200_OK,
        )

    except Exception as err:
        return error_response(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message="Internal server error",
            error=str(err),
        )


async def delete_book(book_id, db):
    try:
        book = await db.books.find_one_and_update(
            {"_id": ObjectId(book_id)},
            {
                "$set": {
                    "isActive": False,
                    "updatedAt": datetime.now(timezone.utc),
                }
            },
        )

        if book is None:
            return error_response(
                status_code=status.HTTP_404_NOT_FOUND,
                message="Book not found",
                error="Book not found",
            )

        return success_response(
            message="Book deleted successfully",
            data=book_id,
            status_code=status.HTTP_200_OK,
        )

    except Exception as err:
        return error_response(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message="Internal server error",
            error=str(err),
        )


async def update_book(book_id, payload, db):
    try:
        update_data = payload.dict(exclude_unset=True)
        book = await db.books.find_one_and_update(
            {"_id": ObjectId(book_id)},
            {
                "$set": {
                    **update_data,
                    "updatedAt": datetime.now(timezone.utc),
                },
            },
            return_document=True,
        )

        if book is None:
            return error_response(
                status_code=status.HTTP_404_NOT_FOUND,
                message="Book not found",
                error="Book not found",
            )

        data = convert_to_serializable(book)

        return success_response(
            message="Book updated successfully",
            data=data,
            status_code=status.HTTP_200_OK,
        )

    except Exception as err:
        return error_response(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message="Internal server error",
            error=str(err),
        )


def test_function(limit, page, is_new, req):
    try:
        json_body = req.json()
        print("req", req)
        print("page", page)
        print("is_new", is_new)
        ab = {"limit": type(limit), "page": type(page), "is_new": type(is_new)}

        obj = {limit, page, is_new}

        print("Query params1...", (ab))
        if limit is not None:
            print(f"We have limit: {limit}")

        if page is not None:
            print(f"We have page: {page}")

        # data = {page, limit}
        data = {
            "page": page,
            "limit": limit,
            "method": req.method,
            "url": str(req.url),
            "headers": dict(req.headers),
            "query_params": dict(req.query_params),
            "client": req.client.host if req.client else None,
        }

        response = success_response(
            status_code=status.HTTP_200_OK, data=data, message="Here is your response"
        )
        response.set_cookie(
            key="token",
            value="123",
        )

        return response

    except Exception as err:
        print("Errro", err)
        return error_response(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message="Internal server error",
            error=str(err),
        )
