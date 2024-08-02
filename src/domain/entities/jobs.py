from dataclasses import dataclass, field

from domain.entities.base import BaseEntity


@dataclass
class JobEntity(BaseEntity):
    title: str
    description: str
    salary_from: float
    salary_to: float
    is_active: bool
    user_id: str
    responses_ids: list[int] = field(default_factory=list)
