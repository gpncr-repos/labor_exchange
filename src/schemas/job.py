import datetime
from typing import Optional
from pydantic import BaseModel


class JobSchema(BaseModel):
    name: str
    user_id: int
    title: str
    description: str
    salary_from: Optional[int]
    salary_to: Optional[int]
    is_active: bool
    create_at: datetime.datetime
