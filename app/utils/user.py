from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import FastAPI, Depends, HTTPException, Request

from motor.motor_asyncio import AsyncIOMotorClient
from app.config.db import connect_to_db
from bson import ObjectId
from app.utils import convert_to_serializable, decode_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


async def get_token(request: Request, token: str = Depends(oauth2_scheme)):
    if token:
        return token

    token_from_cookies = request.cookies.get("access_token")

    if not token_from_cookies:
        raise HTTPException(
            status_code=401,
            detail="Not authenticated",
        )

    return token_from_cookies


async def get_current_user(
    token: str = Depends(get_token), db: AsyncIOMotorClient = Depends(connect_to_db)
):
    try:
        id = decode_token(token, "access").get("_id")

        if not id:
            raise HTTPException(
                status_code=401,
                detail="Not authenticated",
            )

        user = await db.users.find_one({"_id": ObjectId(id)}, {"password": 0})

        if user is None or not user.get("is_active"):
            raise HTTPException(
                status_code=401,
                detail="Not authenticated",
            )

        return convert_to_serializable(user)

    except Exception as err:
        raise HTTPException(
            status_code=401,
            detail="Not authenticated",
        )
