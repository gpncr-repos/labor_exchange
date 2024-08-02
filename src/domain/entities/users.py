from dataclasses import dataclass

from domain.entities.base import BaseEntity


@dataclass
class UserEntity(BaseEntity):
    email: str
    name: str
    is_company: bool
    password: str | None = None
    hashed_password: str | None = None


@dataclass
class TokenEntity:
    access_token: str
    token_type: str
