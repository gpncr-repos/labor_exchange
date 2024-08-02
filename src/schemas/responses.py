import datetime
from typing import Optional

from pydantic import BaseModel


class ResponsesSchema(BaseModel):
    id: int
    user_id: int
    job_id: int
    massage: str
    created_at: datetime.datetime

    class Config:
        orm_mode = True


class ResponsestoSchema(BaseModel):
    user_id: int
    job_id: int
    massage: str

    class Config:
        orm_mode = True


class ResponsesinSchema(BaseModel):
    job_id: int
    massage: str

    class Config:
        orm_mode = True
