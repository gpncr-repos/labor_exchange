import datetime
from typing import Optional
from pydantic import BaseModel


class JobSchema(BaseModel):
    id: str 
    user_id: int
    title: str
    discription: str
    salary_from: int
    salary_to: int
    is_active: bool
    created_at: datetime.datetime

    class Config: #уточнить
        orm_mode = True

class JobtoSchema(BaseModel):
    user_id: int
    title: str
    discription: str
    salary_from: int
    salary_to: int
    is_active: bool
    
    class Config:
        orm_mode = True