""" Shemas of users"""
import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field, validator


class UserSchema(BaseModel):
    """ Shemas as model """
    id: int = Field(examples=[1])
    name: str
    email: EmailStr
    hashed_password: str
    is_company: bool
    created_at: datetime.datetime

    class Config:
        orm_mode = True


class UserGetSchema(BaseModel):
    """ Shemas for get """
    id: int = Field(examples=[1])
    name: str
    email: EmailStr
    is_company: bool
    created_at: datetime.datetime

    class Config:
        orm_mode = True


class UserUpdateSchema(BaseModel):
    """ Shemas for patch """
    name: Optional[str] = Field(examples=['Василий'])
    email: Optional[EmailStr] = Field(examples=['Vasilii@alibabaevich.com'])
    is_company: Optional[bool] = None

    class Config:
        orm_mode = True


class UserCreateSchema(BaseModel):
    """ Shemas for create """
    name: str = Field(examples=['Василий'])
    email: EmailStr = Field(examples=['Vasilii@alibabaevich.com'])
    password: str = Field(min_length=8)
    password2: str = Field(min_length=8)
    is_company: bool = False

    class Config:
        orm_mode = True

    @validator('password2')
    def password_match(cls, v, values, **kwargs):
        if 'password' in values and v != values['password']:
            raise ValueError('Пароли не совпадают!')
        return True
