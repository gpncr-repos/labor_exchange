import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, validator, constr


class ResponseSchema(BaseModel):
    id: Optional[str] = None
    user_id: int
    job_id: int
    message: Optional[str]

    class Config:
        orm_mode = True


class ResponseUpdateSchema(BaseModel):
    user_id: int
    job_id: int
    message: Optional[str]


class ResponseInSchema(BaseModel):
    user_id: int
    job_id: int
    message: Optional[str]
