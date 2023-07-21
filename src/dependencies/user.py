from fastapi import Depends, HTTPException, status, Body
from core.security import oauth2_scheme, decode_token
from queries import user as user_queries
from sqlalchemy.ext.asyncio import AsyncSession
from dependencies.db import get_db
from models import User


async def get_current_user(
    db: AsyncSession = Depends(get_db),
    token: str = Depends(oauth2_scheme)
) -> User:
    if payload := decode_token(token):
        if payload.get("type") == "acc":
            if email := payload.get("sub"):
                if user := await user_queries.get_by_email(db=db, email=email):
                    return user

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Credentials are not valid!"
    )


async def get_user_by_refresh_token(
    db: AsyncSession = Depends(get_db),
    refresh_token: str = Body(embed=True)
) -> User:
    if payload := decode_token(refresh_token):
        if payload.get("type") == "ref":
            if email := payload.get("sub"):
                if user := await user_queries.get_by_email(db=db, email=email):
                    return user

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Invalid refresh token!"
    )
