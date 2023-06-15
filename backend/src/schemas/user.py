import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, validator, constr


class UserSchema(BaseModel):
    id: Optional[int] = None
    name: str
    email: str
    hashed_password: str
    created_at: datetime.datetime

    class Config:
        orm_mode = True


class UserUpdateSchema(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    new_password: Optional[constr(min_length=8)] = None
    password: Optional[constr(min_length=8)] = None


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
