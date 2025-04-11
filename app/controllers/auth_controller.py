from fastapi import HTTPException, status, Response, Request
from app.utils import success_response, error_response
from app.config.settings import settings
from datetime import datetime, timezone
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient
from app.schemas import RegisterSchema, LoginSchema
from app.utils import (
    convert_to_serializable,
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
    decode_token,
)
from app.config.settings import settings


async def get_user_by_email(email: str, db: AsyncIOMotorClient) -> dict:
    return await db.users.find_one({"email": email})


async def create_user(user: RegisterSchema, db: AsyncIOMotorClient):
    try:

        existing_user = await get_user_by_email(user.email, db)
        if existing_user:
            return error_response(
                status_code=status.HTTP_400_BAD_REQUEST,
                message="User already exists",
                error="User with this email already exists",
            )

        hashed_password = hash_password(user.password)
        new_user = {
            "name": user.name,
            "email": user.email,
            "password": hashed_password,
            "refresh_token": None,
            "is_active": True,
            "is_verified": True,
            "token_updated_at": None,
            "last_login": None,
            "created_at": datetime.now(timezone.utc),
            "updated_at": datetime.now(timezone.utc),
        }

        await db.users.insert_one(new_user)

        return success_response(
            status_code=status.HTTP_201_CREATED,
            message="User created successfully",
            data={"email": user.email},
        )

    except Exception as err:
        return error_response(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message="Internal server error",
            error=str(err),
        )


async def login_user(user: LoginSchema, db: AsyncIOMotorClient):
    try:
        existing_user = await get_user_by_email(user.email, db)
        if not existing_user or not verify_password(
            user.password, existing_user["password"]
        ):
            return error_response(
                status_code=status.HTTP_404_NOT_FOUND,
                message="Invalid credentials",
                error="Invalid credentials",
            )
        user = convert_to_serializable(existing_user)
        user_id = user.get("_id")
        access_token = create_access_token(data={"_id": user_id})
        refresh_token = create_refresh_token(data={"_id": user_id})

        print("I am here", access_token)
        print("I am here", refresh_token)

        await db.users.update_one(
            {"_id": ObjectId(user_id)},
            {
                "$set": {
                    "refresh_token": refresh_token,
                    "last_login": datetime.now(timezone.utc),
                    "token_updated_at": datetime.now(timezone.utc),
                    "updated_at": datetime.now(timezone.utc),
                }
            },
        )

        user.pop("password", None)
        response = success_response(
            status_code=status.HTTP_200_OK,
            message="Login successful",
            data=user,
        )
        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            expires=settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60,
            secure=True,
        )
        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            expires=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            secure=True,
        )

        return response

    except Exception as err:
        return error_response(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message="Internal server error",
            error=str(err),
        )


async def refresh_user_token(request: Request, db: AsyncIOMotorClient):
    try:
        # get the refresh token from cookies
        refresh_token = request.cookies.get("refresh_token")
        print("refresh token", refresh_token)
        if not refresh_token:
            return error_response(
                status_code=status.HTTP_401_UNAUTHORIZED,
                message="Unauthorized",
                error="Refresh token not found",
            )

        # decode the refresh token
        payload = decode_token(refresh_token, "refresh")
        user_id = payload.get("_id")

        if not user_id:
            return error_response(
                status_code=status.HTTP_401_UNAUTHORIZED,
                message="Unauthorized",
                error="Invalid refresh token",
            )

        # get the user from the database
        user = await db.users.find_one({"_id": ObjectId(user_id)})
        if not user:
            return error_response(
                status_code=status.HTTP_401_UNAUTHORIZED,
                message="Unauthorized",
                error="User not found",
            )

        # check if the refresh token in the database matches the one in the cookie
        if user["refresh_token"] != refresh_token:
            return error_response(
                status_code=status.HTTP_401_UNAUTHORIZED,
                message="Unauthorized",
                error="Invalid refresh token",
            )

        # create new access token
        access_token = create_access_token(data={"_id": str(user["_id"])})
        # update the token in the database
        await db.users.update_one(
            {"_id": ObjectId(user["_id"])},
            {"$set": {"token_updated_at": datetime.now(timezone.utc)}},
        )

        # set the new access token in the response cookies
        response = success_response(
            status_code=status.HTTP_200_OK, message="Token refreshed successfully"
        )
        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            expires=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        )
        return response

    except Exception as err:
        return error_response(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message="Internal server error",
            error=str(err),
        )


async def logout_user(user: dict, db: AsyncIOMotorClient):
    try:
        await db.users.update_one(
            {"_id": ObjectId(user["_id"])},
            {
                "$set": {
                    "refresh_token": None,
                    "updated_at": datetime.now(timezone.utc),
                    "token_updated_at": None,
                }
            },
        )

        response = success_response(
            status_code=status.HTTP_200_OK, message="Logout successful"
        )

        response.delete_cookie(key="refresh_token")
        response.delete_cookie(key="access_token")

        return response
    except Exception as err:
        return error_response(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message="Internal server error",
            error=str(err),
        )
