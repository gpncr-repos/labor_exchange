"""Схемы объектов для аутентификации пользователей"""
from pydantic import BaseModel, EmailStr


class TokenSchema(BaseModel):
    """Класс, хранящий токен и его тип"""
    token: str
    token_type: str

class TokenSchemaPair(BaseModel):
    """Класс, хранящий access и refresh токены для доступа"""
    access_token: TokenSchema
    refresh_token: TokenSchema

class LoginSchema(BaseModel):
    """Схема для эндпоинта авторизации: логин (адрес эл.почты) и пароль"""
    email: EmailStr
    password: str
