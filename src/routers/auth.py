from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.security import create_access_token, verify_password
from dependencies import get_db
from queries import user as user_queries
from schemas import LoginSchema, TokenSchema

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("", response_model=TokenSchema)
async def login(login: LoginSchema, db: AsyncSession = Depends(get_db)):
    user = await user_queries.get_by_email(db=db, email=login.email)

    if user is None or not verify_password(login.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Некорректное имя пользователя или пароль",
        )

    return TokenSchema(access_token=create_access_token({"sub": user.email}), token_type="Bearer")
