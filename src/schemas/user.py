import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, validator, constr


class UserSchema(BaseModel):
    id: Optional[int] = None
    name: str
    email: EmailStr
    hashed_password: str
    is_company: bool
    created_at: datetime.datetime

    class Config:
        from_attributes = True


class UserUpdateSchema(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    is_company: Optional[bool] = None


class UserInSchema(BaseModel):
    name: str
    email: EmailStr
    password: constr(min_length=8)
    password2: str
    is_company: bool = False

    @validator("password2")
    def password_match(cls, v, values, **kwargs):
        if 'password' in values and v != values["password"]:
            raise ValueError("Пароли не совпадают!")
        return True
