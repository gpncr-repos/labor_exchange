from dataclasses import dataclass

from domain.entities.base import BaseEntity


@dataclass
class JobEntity(BaseEntity):
    title: str
    description: str
    salary_from: float
    salary_to: float
    is_active: bool
    user_id: int
    responses_ids: list[int]
