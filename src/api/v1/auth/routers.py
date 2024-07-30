from fastapi import APIRouter, HTTPException, status, Depends
from punq import Container

from api.v1.auth.schemas import TokenSchema, LoginSchema
from di import get_container
from core.exceptions import ApplicationException
from logic.services.users.base import BaseUserService

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("", response_model=TokenSchema)
async def login(
        login: LoginSchema,
        container: Container = Depends(get_container)
) -> TokenSchema:
    service: BaseUserService = container.resolve(BaseUserService)
    try:
        token = await service.login_user(email=login.email, password=login.password)
    except ApplicationException as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=e.message,
        )

    return TokenSchema.from_entity(token)
