from typing import Optional

from pydantic import BaseModel


class JobInSchema(BaseModel):
    title: str
    description: Optional[str]
    salary_from: Optional[int]
    salary_to: Optional[int]


class JobUpdateSchema(BaseModel):
    title: Optional[str]
    description: Optional[str]
    salary_from: Optional[int]
    salary_to: Optional[int]


class JobSchema(BaseModel):
    id: int
    title: str
    description: Optional[str]
    salary_from: Optional[int]
    salary_to: Optional[int]

    class Config:
        orm_mode = True
