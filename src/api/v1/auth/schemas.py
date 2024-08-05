from datetime import datetime

from pydantic import BaseModel, EmailStr

from domain.entities.auth import TokenEntity, TokenPayloadEntity


class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str | None = None
    token_type: str

    @classmethod
    def from_entity(cls, entity: TokenEntity) -> "TokenSchema":
        return cls(
            access_token=entity.access_token,
            refresh_token=entity.refresh_token,
            token_type=entity.token_type, )


class RefreshTokenSchema(BaseModel):
    refresh_token: str


class TokenPayloadSchema(BaseModel):
    sub: str
    iat: datetime

    @staticmethod
    def from_entity(entity: TokenPayloadEntity) -> 'TokenPayloadSchema':
        return TokenPayloadSchema(
            sub=entity.sub,
            iat=entity.iat,
        )


class LoginSchema(BaseModel):
    email: EmailStr
    password: str
