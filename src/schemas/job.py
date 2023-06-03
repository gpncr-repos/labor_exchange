from decimal import Decimal
from typing import Optional
from pydantic import BaseModel, Field


class JobInSchema(BaseModel):
    title: str
    description: Optional[str]
    salary_from: Optional[float]
    salary_to: Optional[float]

    class Config:
        schema_extra = {
            "example": {
                "title": "Ведущий разработчик Python в ГПН ЦР",
                "description": "Требуется разработчик с опытом 10 лет",
                "salary_from": 300000,
                "salary_to": 400000,
            }
        }


class JobSchema(BaseModel):
    id: Optional[int] = None
    title: str
    description: Optional[str]
    is_active: bool
    salary_from: Optional[float]
    salary_to: Optional[float]

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id": 1,
                "title": "Ведущий разработчик Python в ГПН ЦР",
                "description": "Требуется разработчик с опытом 10 лет",
                "salary_from": 300000,
                "salary_to": 400000,
            }
        }
