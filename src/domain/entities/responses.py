from dataclasses import dataclass

from domain.entities.base import BaseEntity
from domain.entities.jobs import JobEntity
from domain.entities.users import UserEntity


@dataclass
class ResponseEntity(BaseEntity):
    message: str
    user_id: str
    job_id: str


@dataclass
class ResponseAggregateJobEntity(BaseEntity):
    message: str
    user_id: str
    job_id: str
    job: JobEntity


@dataclass
class ResponseAggregateUserEntity(BaseEntity):
    message: str
    user_id: str
    job_id: str
    user: UserEntity
