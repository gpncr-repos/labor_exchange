from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from queries import UserRepository

from schemas import TokenSchema, LoginSchema
from core.security import verify_password, create_access_token
from dependencies import get_db


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("", response_model=TokenSchema)
async def login(login: LoginSchema, db: AsyncSession = Depends(get_db)):
    user_repo = UserRepository()
    user = await user_repo.get_single(db, email=login.email)

    if user is None or not verify_password(login.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Некорректное имя пользователя или пароль")

    return TokenSchema(
        access_token=create_access_token({"sub": user.email}),
        token_type="Bearer"
    )
