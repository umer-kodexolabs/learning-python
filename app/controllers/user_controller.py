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


async def get_user_by_email(user):
    try:
        return success_response(
            message="User fetched successfully",
            data=user,
            status_code=status.HTTP_200_OK,
        )

    except Exception as err:
        return error_response(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message="Internal server error",
            error=str(err),
        )
