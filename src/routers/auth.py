from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.security import (JWTBearer, create_access_token,
                           create_refresh_token, decode_token, verify_password)
from dependencies import get_db
from queries import user as user_queries
from schemas import AccessTokensSchema, LoginSchema, TokenSchema

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("", response_model=AccessTokensSchema)
async def login(login: LoginSchema, db: AsyncSession = Depends(get_db)):
    user = await user_queries.get_by_email(db=db, email=login.email)

    if user is None or not verify_password(login.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Некорректное имя пользователя или пароль",
        )

    return AccessTokensSchema(
        access_token=TokenSchema(
            token=create_access_token({"sub": user.email}), token_type="Bearer"
        ),
        refresh_token=TokenSchema(
            token=create_refresh_token({"sub": user.email}), token_type="Bearer"
        ),
    )


@router.post("/refresh", response_model=TokenSchema)
async def get_new_access_token(
    refresh_token: str = Depends(JWTBearer()), db: AsyncSession = Depends(get_db)
):

    decode_refresh_token = decode_token(refresh_token)

    if decode_refresh_token is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="невалидный токен"
        )
    else:
        current_user = await user_queries.get_by_email(
            db=db, email=decode_refresh_token.get("sub")
        )
        return TokenSchema(
            token=create_access_token({"sub": current_user.email}), token_type="Bearer"
        )
