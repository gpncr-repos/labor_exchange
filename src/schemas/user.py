import datetime

from pydantic import BaseModel, EmailStr, validator


class UserSchema(BaseModel):
    class Config:
        orm_mode = True

    id: str | None = None
    name: str
    email: EmailStr
    # не стоит отправлять хэш пароля, если он все-таки где-то понадобится, можно
    # будет отнаследовать новую модель от UserSchema и добавить атрибут hashed_password
    is_company: bool
    created_at: datetime.datetime


class UserUpdateSchema(BaseModel):
    name: str | None = None
    email: EmailStr | None = None
    is_company: bool | None = None


class UserInSchema(BaseModel):
    name: str
    email: EmailStr
    password: str
    password2: str
    is_company: bool = False

    @validator("password", pre=True)
    def validate_password(cls, value):
        if len(value) < 8:
            raise ValueError("Пароль должен быть не короче 8 символов.")
        return value

    @validator("password2")
    def password_match(cls, v, values):
        if "password" in values and v != values["password"]:
            raise ValueError("Пароли не совпадают!")
        return True
