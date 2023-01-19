from fastapi import Depends, HTTPException, status
from core.security import JWTBearer, decode_access_token
from sqlalchemy.ext.asyncio import AsyncSession
from dependencies.db import get_db
from models import User
from queries.user import UserRepository


async def get_current_user(db: AsyncSession = Depends(get_db), token: str = Depends(JWTBearer())) -> User:
    cred_exception = HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Credentials are not valid")
    user_repo = UserRepository()
    payload = decode_access_token(token)
    if payload is None:
        raise cred_exception
    email: str = payload.get("sub")
    if email is None:
        raise cred_exception
    user = await user_repo.get_single(db=db, email=email)
    if user is None:
        raise cred_exception
    return user


async def get_current_employee(user: User = Depends(get_current_user)) -> User:
    if user.is_company:
        raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED, detail="Method not allowed")
    return user


async def get_current_employer(user: User = Depends(get_current_user)) -> User:
    if not user.is_company:
        raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED, detail="Method not allowed")
    return user
