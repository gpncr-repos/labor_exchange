from pydantic import BaseModel, EmailStr


class TokenSchema(BaseModel):
    token: str
    token_type: str


class LoginSchema(BaseModel):
    email: EmailStr
    password: str


class AccessTokensSchema(BaseModel):
    access_token: TokenSchema
    refresh_token: TokenSchema
