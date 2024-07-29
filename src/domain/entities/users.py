from dataclasses import dataclass

from domain.entities.base import BaseEntity


@dataclass
class UserEntity(BaseEntity):
    email: str
    name: str
    is_company: bool
    password: str | None = None
    hashed_password: bytes | None = None
    jobs_ids: list[int] | None = None
    responses_ids: list[int] | None = None
