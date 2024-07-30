from pydantic import BaseModel, EmailStr

from domain.entities.users import TokenEntity


class TokenSchema(BaseModel):
    access_token: str
    token_type: str

    @classmethod
    def from_entity(cls, entity: TokenEntity) -> "TokenSchema":
        return cls(access_token=entity.access_token, token_type=entity.token_type,)


class LoginSchema(BaseModel):
    email: EmailStr
    password: str