from fastapi import APIRouter, HTTPException, status, Depends

from api.dependencies.users import get_user_service
from api.v1.auth.schemas import TokenSchema, LoginSchema
from core.exceptions import ApplicationException
from logic.services.users.base import BaseUserService

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("", response_model=TokenSchema)
async def login(
        login: LoginSchema,
        user_service: BaseUserService = Depends(get_user_service)
) -> TokenSchema:
    try:
        token = await user_service.login_user(email=login.email, password=login.password)
    except ApplicationException as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=e.message,
        )

    return TokenSchema.from_entity(token)
