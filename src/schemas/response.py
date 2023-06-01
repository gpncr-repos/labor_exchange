from typing import Optional
from pydantic import BaseModel


class ResponseInSchema(BaseModel):
    job_id: int
    user_id: int
    message: Optional[str]


class ResponseSchema(BaseModel):
    id: Optional[int] = None
    job_id: int
    user_id: int
    message: Optional[str]

    class Config:
        orm_mode = True
