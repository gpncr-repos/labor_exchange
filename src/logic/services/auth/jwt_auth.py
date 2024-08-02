from dataclasses import asdict
from datetime import timedelta

from jose.exceptions import JWSError

from core.config import settings
from domain.entities.auth import TokenPayloadEntity, TokenEntity
from domain.entities.users import UserEntity
from infra.repositories.users.base import BaseUserRepository
from logic.exceptions.auth import InvalidTokenException, InvalidTokenTypeException, WrongCredentialsException
from logic.utils import auth as auth_utils
from logic.utils.auth import validate_token_type, verify_password


class JWTAuthService:
    def __init__(self, user_repository: BaseUserRepository):
        self.user_repository = user_repository

    @staticmethod
    def create_jwt(
            token_type: str,
            token_data: dict,
            expire_minutes: int = settings.auth_jwt.access_token_expire_minutes,
            expire_timedelta: timedelta | None = None,
    ) -> str:
        jwt_payload = {settings.auth_jwt.token_type_field_name: token_type}
        jwt_payload.update(token_data)
        return auth_utils.encode_jwt(
            payload=jwt_payload,
            expire_minutes=expire_minutes,
            expire_timedelta=expire_timedelta,
        )

    def create_access_token(self, user: UserEntity) -> str:
        jwt_payload = TokenPayloadEntity(
            sub=user.email,
        )
        return self.create_jwt(
            token_type=settings.auth_jwt.access_token_name,
            token_data=asdict(jwt_payload),
            expire_minutes=settings.auth_jwt.access_token_expire_minutes,
        )

    def create_refresh_token(self, user: UserEntity) -> str:
        jwt_payload = TokenPayloadEntity(
            sub=user.email,
        )
        return self.create_jwt(
            token_type=settings.auth_jwt.refresh_token_name,
            token_data=asdict(jwt_payload),
            expire_timedelta=timedelta(days=settings.auth_jwt.refresh_token_expire_days),
        )

    @staticmethod
    def get_token_payload(token: str, token_type: str) -> TokenPayloadEntity:
        try:
            payload = auth_utils.decode_jwt(token=token)
        except JWSError:
            raise InvalidTokenException
        if not validate_token_type(payload, token_type):
            raise InvalidTokenTypeException(token_type)
        if not (email := payload["sub"]):
            raise InvalidTokenException
        return TokenPayloadEntity(
            sub=email,
            iat=payload["iat"],
        )

    async def login_user(self, email: str, password: str):

        user = await self.user_repository.get_one_by_email(email=email)

        if not verify_password(password, user.hashed_password):
            raise WrongCredentialsException

        return TokenEntity(
            access_token=self.create_access_token(user=user.to_entity()),
            refresh_token=self.create_refresh_token(),
            token_type="Bearer"
        )
