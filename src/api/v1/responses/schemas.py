from pydantic import BaseModel

from api.v1.jobs.schemas import JobSchema
from api.v1.users.schemas import UserSchema
from domain.entities.responses import ResponseEntity, ResponseAggregateJobEntity, ResponseAggregateUserEntity


class ResponseCreateSchema(BaseModel):
    message: str
    job_id: str
    user_id: str | None = None

    def to_entity(self) -> ResponseEntity:
        return ResponseEntity(
            message=self.message,
            job_id=self.job_id,
            user_id=self.user_id,
        )


class ResponseSchema(BaseModel):
    id: str
    message: str
    job_id: str
    user_id: str

    @classmethod
    def from_entity(cls, response: ResponseEntity) -> "ResponseSchema":
        return ResponseSchema(
            id=response.id,
            message=response.message,
            job_id=response.job_id,
            user_id=response.user_id,
        )


class ResponseAggregateJobSchema(BaseModel):
    id: str
    message: str
    job_id: str
    user_id: str
    job: JobSchema

    @classmethod
    def from_entity(cls, response: ResponseAggregateJobEntity) -> "ResponseAggregateJobSchema":
        return ResponseAggregateJobSchema(
            id=response.id,
            message=response.message,
            job_id=response.job_id,
            user_id=response.user_id,
            job=JobSchema.from_entity(response.job)
        )


class ResponseAggregateUserSchema(BaseModel):
    id: str
    message: str
    job_id: str
    user_id: str
    user: UserSchema

    @classmethod
    def from_entity(cls, response: ResponseAggregateUserEntity) -> "ResponseAggregateUserSchema":
        return ResponseAggregateUserSchema(
            id=response.id,
            message=response.message,
            job_id=response.job_id,
            user_id=response.user_id,
            user=UserSchema.from_entity(response.user)
        )
