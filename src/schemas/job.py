import datetime
from typing import Optional
from pydantic import BaseModel


class JobSchema(BaseModel):
    id: Optional[int] = None
    user_id: int
    title: str
    description: str
    salary_from: Optional[int]
    salary_to: Optional[int]
    is_active: bool
    created_at: datetime.datetime

    class Config:
        orm_mode = True


class JobInputSchema(BaseModel):
    title: str
    description: str
    salary_from: Optional[int]
    salary_to: Optional[int]
    is_active: bool