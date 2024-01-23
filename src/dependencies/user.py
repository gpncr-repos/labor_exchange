from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.security import JWTBearer, decode_access_token
from src.database.tables import User
from src.dependencies.database import get_session
from src.queries import user as user_queries


async def get_current_user(db: AsyncSession = Depends(get_session), token: str = Depends(JWTBearer())) -> User:
    cred_exception = HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Credentials are not valid")
    payload = decode_access_token(token)
    if payload is None:
        raise cred_exception
    email: str = payload.get("sub")
    if email is None:
        raise cred_exception
    user = await user_queries.get_by_email(session=db, email=email)
    if user is None:
        raise cred_exception
    return user
