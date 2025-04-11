from fastapi import APIRouter, Depends, Request
from motor.motor_asyncio import AsyncIOMotorClient
from app.config.db import connect_to_db
from app.controllers.auth_controller import create_user, login_user, refresh_user_token
from app.schemas import RegisterSchema, LoginSchema


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/sign-up")
async def register(
    payload: RegisterSchema, db: AsyncIOMotorClient = Depends(connect_to_db)
):
    return await create_user(payload, db)


@router.post("/sign-in")
async def login(payload: LoginSchema, db: AsyncIOMotorClient = Depends(connect_to_db)):
    return await login_user(payload, db)


@router.get("/refresh-token")
async def refresh_token(
    request: Request, db: AsyncIOMotorClient = Depends(connect_to_db)
):
    print("I am here")
    return await refresh_user_token(request, db)
