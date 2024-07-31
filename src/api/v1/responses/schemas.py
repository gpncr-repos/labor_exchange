from pydantic import BaseModel

from api.v1.jobs.schemas import JobSchema
from domain.entities.responses import ResponseEntity, ResponseDetailEntity


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


class ResponseDetailSchema(BaseModel):
    message: str
    job_id: str
    user_id: str
    job: JobSchema

    @classmethod
    def from_entity(cls, response: ResponseDetailEntity) -> "ResponseDetailSchema":
        return ResponseDetailSchema(
            id=response.id,
            message=response.message,
            job_id=response.job_id,
            user_id=response.user_id,
            job=JobSchema.from_entity(response.job)
        )
