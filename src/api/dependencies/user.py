from fastapi import Depends, HTTPException, status

from infra.repositories.alchemy_settings import get_session
from infra.repositories.users.alchemy import AlchemyUserRepository
from logic.utils.security import JWTBearer, decode_access_token
from sqlalchemy.ext.asyncio import AsyncSession


async def get_current_user(session: AsyncSession = Depends(get_session), token: str = Depends(JWTBearer())):
    cred_exception = HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Credentials are not valid")
    payload = decode_access_token(token)
    if payload is None:
        raise cred_exception
    email: str = payload.get("sub")
    if email is None:
        raise cred_exception
    repo = AlchemyUserRepository(session)
    user = await repo.get_by_email(email=email)
    if user is None:
        raise cred_exception
    return user.to_entity()
