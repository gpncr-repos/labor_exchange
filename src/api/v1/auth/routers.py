from fastapi import APIRouter, HTTPException, status, Depends

from api.dependencies.auth import get_auth_service
from api.dependencies.users import get_user_service
from api.v1.auth.schemas import TokenSchema, LoginSchema, RefreshTokenSchema
from core.config import settings
from core.exceptions import ApplicationException
from logic.services.auth.jwt_auth import JWTAuthService
from logic.services.users.base import BaseUserService

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=TokenSchema)
async def login(
        creds: LoginSchema,
        auth_service: JWTAuthService = Depends(get_auth_service)
) -> TokenSchema:
    try:
        token = await auth_service.login_user(email=creds.email, password=creds.password)
    except ApplicationException as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=e.message,
        )
    return TokenSchema.from_entity(token)


@router.post(
    "/refresh",
    response_model=TokenSchema,
)
async def refresh_token(
        token: RefreshTokenSchema,
        auth_service: JWTAuthService = Depends(get_auth_service),
        user_service: BaseUserService = Depends(get_user_service),
) -> TokenSchema:
    try:
        payload = auth_service.get_token_payload(
            token=token.refresh_token,
            token_type=settings.auth_jwt.refresh_token_name
        )
        user = await user_service.get_user_by_email(email=payload.sub)
        access_token = auth_service.create_access_token(user=user)
        refresh_token = auth_service.create_refresh_token(user=user)
    except ApplicationException as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=e.message,
        )
    return TokenSchema(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type=settings.auth_jwt.token_type_field_name,
    )
