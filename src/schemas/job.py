from decimal import Decimal
from typing import Optional
from pydantic import BaseModel


class JobInSchema(BaseModel):
    title: str
    description: Optional[str]  # str or None
    salary_from: Optional[Decimal]
    salary_to: Optional[Decimal]


class JobSchema(BaseModel):
    id: Optional[int] = None
    title: str
    description: Optional[str]
    salary_from: Optional[Decimal]
    salary_to: Optional[Decimal]

    class Config:
        orm_mode = True
