from fastapi import Depends, Request, HTTPException, status
from fastapi.security import HTTPBearer
from punq import Container

from api.dependencies.users import get_user_service
from core.config import settings
from core.exceptions import ApplicationException
from domain.entities.users import UserEntity
from logic.services.users.base import BaseUserService
from logic.services.auth.jwt_auth import JWTAuthService
from di import get_container
from logic.utils.auth import decode_jwt


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            try:
                decode_jwt(credentials.credentials)
            except ApplicationException as e:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=e.message)
            return credentials.credentials
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid auth token")


def get_auth_service(container: Container = Depends(get_container)) -> JWTAuthService:
    service: JWTAuthService = container.resolve(JWTAuthService)
    return service


async def get_auth_user(
        auth_service: JWTAuthService = Depends(get_auth_service),
        user_service: BaseUserService = Depends(get_user_service),
        token: str = Depends(JWTBearer())
) -> UserEntity:
    try:
        payload = auth_service.get_token_payload(token, settings.auth_jwt.access_token_name)
        user = await user_service.get_user_by_email(email=payload.sub)
    except ApplicationException as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=e.message)
    return user
