from fastapi import Depends, HTTPException, status
from core.security import JWTBearer, decode_token
from applications.queries import user_queries as user_queries
from sqlalchemy.ext.asyncio import AsyncSession
from applications.dependencies.db import get_db
from domain.do_schemas import DOUser
from models.users import User


async def get_current_user(
        db: AsyncSession = Depends(get_db),
        token: str = Depends(JWTBearer())) -> DOUser:
    cred_exception = HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Credentials не валидны")
    payload = decode_token(token)
    if payload is None:
        raise cred_exception
    email: str = payload.get("sub")
    if email is None:
        raise cred_exception
    user = await user_queries.get_by_email(db=db, email=email)
    if user is None:
        raise cred_exception
    return user
