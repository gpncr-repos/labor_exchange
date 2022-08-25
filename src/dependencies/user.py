from fastapi import Depends, HTTPException, status
from core.security import JWTBearer, decode_access_token
from queries import user as user_queries
from sqlalchemy.ext.asyncio import AsyncSession
from dependencies.db import get_db
from models import User


async def get_current_user(db: AsyncSession = Depends(get_db), token: str = Depends(JWTBearer())) -> User:
    cred_exception = HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Credentials are not valid")
    payload = decode_access_token(token)
    if payload is None:
        raise cred_exception
    email: str = payload.get("sub")
    if email is None:
        raise cred_exception
    user = await user_queries.get_by_email(db=db, email=email)
    if user is None:
        raise cred_exception
    return user
