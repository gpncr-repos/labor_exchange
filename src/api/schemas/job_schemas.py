import random
from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, Field


class SJob(BaseModel):
    # user_id: int = Field(description="Идентифкатор работодателя")
    title: Optional[str] = Field(description="Наименование вакансии")
    description: Optional[str] = Field(description="Описание вакансии")
    salary_from: Optional[Decimal] = Field(description="Зарплата от", ge=0.)
    salary_to: Optional[Decimal] = Field(description="Зарплата до", ge=0.)
    is_active: Optional[bool] = Field(default=True,description="Активна ли вакансия")
    # created_at: Optional[str] = Field(default=datetime.strftime(datetime.utcnow(), "%Y-%m-%d %H-%M-%S"), description="Наименование вакансии")

    class Config:
        schema_extra = {
            "example":
                {
                    # "user_id": int(random.randint(1,100)),
                    "title": "some_title",
                    "description": "some_description",
                    "salary_from": 1.,
                    "salary_to": 10.,
                    "is_active": True,
                    # "created_at": datetime.strftime(datetime.utcnow(), "%Y-%m-%d %H:%M:%S"),
                }
        }

# class SJobs(BaseModel):
#     vacancies: Optional[list[SJob]] = Field(default_factory=list, description="Список вакансий")

class SimpleTextReport(BaseModel):
    message: Optional[str] = "Запрос выполнен"

class SRemoveJobReport(SimpleTextReport):
    pass
