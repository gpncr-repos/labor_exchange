from pydantic import BaseModel, EmailStr


class TokenSchema(BaseModel):
    id: int
    is_company: bool
    access_token: str


class LoginSchema(BaseModel):
    email: EmailStr
    password: str