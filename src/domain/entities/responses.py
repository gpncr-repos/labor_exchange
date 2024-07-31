from dataclasses import dataclass

from domain.entities.base import BaseEntity
from domain.entities.jobs import JobEntity


@dataclass
class ResponseEntity(BaseEntity):
    message: str
    user_id: str
    job_id: str


@dataclass
class ResponseDetailEntity(BaseEntity):
    message: str
    user_id: str
    job_id: str
    job: JobEntity
