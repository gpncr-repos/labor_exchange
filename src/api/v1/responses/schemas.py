from pydantic import BaseModel, Field

from domain.entities.responses import ResponseEntity


class ResponseSchema(BaseModel):
    message: str
    job_id: str
    user_id: str

    def to_entity(self) -> ResponseEntity:
        return ResponseEntity(
            message=self.message,
            job_id=self.job_id,
            user_id=self.user_id,
        )

    @classmethod
    def from_entity(cls, response: ResponseEntity) -> "ResponseSchema":
        return ResponseSchema(
            id=response.id,
            message=response.message,
            job_id=response.job_id,
            user_id=response.user_id,
        )