from pydantic import BaseModel, EmailStr


class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class LoginSchema(BaseModel):
    email: EmailStr
    password: str
