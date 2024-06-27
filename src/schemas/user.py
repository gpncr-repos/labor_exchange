import datetime
from typing import Optional
from pydantic import StringConstraints, BaseModel, EmailStr, field_validator, ConfigDict
from typing_extensions import Annotated


class UserSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: Optional[int] = None
    name: str
    email: EmailStr
    hashed_password: str
    is_company: bool
    created_at: datetime.datetime


class UserUpdateSchema(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    is_company: Optional[bool] = None


class UserInSchema(BaseModel):
    name: str
    email: EmailStr
    password: Annotated[str, StringConstraints(min_length=8)]
    password2: str
    is_company: bool = False

    @field_validator("password2")
    def password_match(cls, v, values, **kwargs) -> str:
        if 'password' in values.data and v != values.data["password"]:
            raise ValueError("Пароли не совпадают!")
        return v
