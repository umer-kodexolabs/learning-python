from fastapi import APIRouter, Depends
from motor.motor_asyncio import AsyncIOMotorClient
from app.config.db import connect_to_db
from app.controllers.user_controller import get_user
from app.utils import get_current_user

router = APIRouter(prefix="/user", tags=["user"])


@router.get("/")
async def user(
    user: dict = Depends(get_current_user),
    db: AsyncIOMotorClient = Depends(connect_to_db),
):
    print("I am here")
    return await get_user(user)
