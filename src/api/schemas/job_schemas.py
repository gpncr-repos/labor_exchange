import random
from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, Field


class SJob(BaseModel):
    """Схема вакансии, получаемая и возвращаемая"""
    user_id: Optional[int] = Field(None, description="Идентифкатор работодателя")
    title: Optional[str] = Field(description="Наименование вакансии")
    description: Optional[str] = Field(description="Описание вакансии")
    salary_from: Optional[Decimal] = Field(description="Зарплата от", ge=0.)
    salary_to: Optional[Decimal] = Field(description="Зарплата до", ge=0.)
    is_active: Optional[bool] = Field(default=True,description="Активна ли вакансия")
    created_at: Optional[datetime] = Field(None, description="Дата создани вакансии")

    class Config:
        orm_mode = True
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


class SimpleTextReport(BaseModel):
    """Короткое текстовое сообщение, ответ о простом действии с базой"""
    id: Optional[int] = None
    message: Optional[str] = "Запрос выполнен"

class SRemoveJobReport(SimpleTextReport):
    """Сообщение об удалении вакансии"""
    pass
