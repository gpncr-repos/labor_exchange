from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

import src.queries.user as user_queries
from src.core.security import create_access_token, verify_password
from src.dependencies import get_session
from src.schemas import LoginSchema, TokenSchema

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("", response_model=TokenSchema)
async def login(login: LoginSchema, db: AsyncSession = Depends(get_session)):
    user = await user_queries.get_by_email(session=db, email=login.email)

    if user is None or not verify_password(login.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Некорректное имя пользователя или пароль")

    return TokenSchema(access_token=create_access_token({"sub": user.email}), token_type="Bearer")
