import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, field_validator, StringConstraints, ValidationInfo

from domain.entities.users import UserEntity


class UserSchema(BaseModel):
    id: Optional[str] = None
    name: str
    email: EmailStr
    is_company: bool
    created_at: datetime.datetime

    class ConfigDict:
        from_attributes = True

    @classmethod
    def from_entity(cls, entity: UserEntity) -> "UserSchema":
        return UserSchema(
            id=entity.id,
            name=entity.name,
            email=entity.email,
            is_company=entity.is_company,
            created_at=entity.created_at,
        )


class UserUpdateSchema(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    is_company: Optional[bool] = None

    def to_entity(self):
        return UserEntity(
            name=self.name,
            email=self.email,
            is_company=self.is_company
        )


class UserInSchema(BaseModel):
    name: str
    email: EmailStr
    password: str
    password2: str
    is_company: bool = False

    @field_validator("password2")
    def password_match(cls, v, info: ValidationInfo):
        if 'password' in info.data and v != info.data["password"]:
            raise ValueError("Пароли не совпадают!")
        return v

    def to_entity(self):
        return UserEntity(
            name=self.name,
            email=self.email,
            password=self.password,
            is_company=self.is_company
        )
