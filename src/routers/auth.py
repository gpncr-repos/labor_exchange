from fastapi import APIRouter, HTTPException, status, Depends, Body
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from queries import user as user_queries

from models import User
from schemas import TokenSchema
from core.security import verify_password, create_token
from dependencies import get_db, get_user_by_refresh_token

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("", response_model=TokenSchema)
async def login(
    login: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):
    user = await user_queries.get_by_email(db=db, email=login.username)

    if user is None or not verify_password(login.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Некорректное имя пользователя или пароль"
        )

    return TokenSchema(
        access_token=create_token({"sub": user.email}),
        refresh_token=create_token({"sub": user.email}, refresh=True),
        token_type="Bearer"
    )


@router.post("/refresh-token", response_model=TokenSchema)
async def refresh_token(
    user: User = Depends(get_user_by_refresh_token)
):
    return TokenSchema(
        access_token=create_token({"sub": user.email}),
        refresh_token=create_token({"sub": user.email}, refresh=True),
        token_type="Bearer"
    )
