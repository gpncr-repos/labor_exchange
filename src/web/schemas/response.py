from typing import Optional

from pydantic import BaseModel

class ResponseSchema(BaseModel):
    id: int | None = None
    job_id: int
    user_id: int
    message: str


class ResponseCreateSchema(BaseModel):
    id: int | None = None
    job_id: int
    user_id: int
    message: str


class ResponseUpdateSchema(BaseModel):
    # что-то сложно увидеть сценарий, когда захочется менять job id или user id
    id: int | None = None
    job_id: int
    user_id: int
    message: str
