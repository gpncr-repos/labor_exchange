from dataclasses import dataclass

from domain.entities.base import BaseEntity


@dataclass
class ResponseEntity(BaseEntity):
    message: str
    user_id: int
    job_id: int
