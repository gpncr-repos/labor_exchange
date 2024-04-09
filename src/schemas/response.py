from typing import Optional
from pydantic import BaseModel


class ResponseSchema(BaseModel):
    id: Optional[int] = None
    user_id: int
    job_id: int
    message: str

    class Config:
        orm_mode = True


class ResponseUpdateSchema(BaseModel):
    user_id: Optional[int] = None
    job_id: Optional[int] = None
    message: Optional[str]


class ResponseInSchema(BaseModel):
    message: Optional[str]
