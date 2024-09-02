from typing import Optional

from pydantic import BaseModel, EmailStr, constr, model_validator
from typing_extensions import Self


class UserSchema(BaseModel):
    id: Optional[int] = None
    name: str
    email: EmailStr
    is_company: bool


class UserUpdateSchema(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    is_company: Optional[bool] = None


class UserCreateSchema(BaseModel):
    name: str
    email: EmailStr
    password: constr(min_length=8)
    password2: str
    is_company: bool = False

    @model_validator(mode="after")
    def password_match(self) -> Self:
        pw1 = self.password
        pw2 = self.password2
        if pw1 is not None and pw2 is not None and pw1 != pw2:
            raise ValueError("passwords do not match")
        return self
