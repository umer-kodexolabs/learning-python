from fastapi import APIRouter, Depends
from motor.motor_asyncio import AsyncIOMotorClient
from app.config.db import connect_to_db
from app.controllers.auth_controller import create_user
from app.schemas import RegisterSchema, LoginSchema


router = APIRouter(prefix="/auth", tags=["auth"])


@router.get("/register")
async def register(
    user: RegisterSchema, db: AsyncIOMotorClient = Depends(connect_to_db)
):
    return await create_user(user, db)
