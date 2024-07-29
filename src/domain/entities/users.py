from dataclasses import dataclass

from domain.entities.base import BaseEntity


@dataclass
class UserEntity(BaseEntity):
    email: str
    name: str
    password: str
    hashed_password: bytes
    is_company: bool
    jobs_ids: list[int]
    responses_ids: list[int]
