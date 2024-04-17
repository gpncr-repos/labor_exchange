import datetime
from typing import Optional

from pydantic import BaseModel, root_validator, validator


class JobSchema(BaseModel):

    id: Optional[int] = None
    user_id: int
    title: str
    description: str
    salary_from: Optional[float] = None
    salary_to: Optional[float] = None
    is_active: bool
    created_at: datetime.datetime

    class Config:
        orm_mode = True


class JobInSchema(BaseModel):
    title: str
    description: str
    salary_from: Optional[float] = None
    salary_to: Optional[float] = None

    @validator("title", "description")
    def check_not_empty(cls, v):
        if not v:
            raise ValueError("Название или описание вакансии не должно быть пустым!")
        return v

    @validator("salary_from", "salary_to")
    def salary_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError("Зарплата не может быть <= 0")
        return v

    @validator("salary_to")
    def check_meaning_of_salary(cls, v, values, **kwargs):
        if "salary_from" in values and v < values["salary_from"]:
            raise ValueError('"Зарплата от" не может быть больше "Зарплаты до"!')
        return v


class JobUpdateSchema(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    salary_from: Optional[float] = None
    salary_to: Optional[float] = None

    @validator("title", "description")
    def check_not_empty(cls, v):
        if v is not None and not v:
            raise ValueError("Название или описание вакансии не должно быть пустым!")
        return v

    @validator("salary_from", "salary_to")
    def salary_must_be_positive(cls, v):
        if v is not None and v <= 0:
            raise ValueError("Зарплата не может быть <= 0")
        return v

    @root_validator
    def check_meaning_of_salary(cls, values):
        salary_from = values.get("salary_from")
        salary_to = values.get("salary_to")
        if salary_from is not None and salary_to is not None:
            if salary_to < salary_from:
                raise ValueError('"Зарплата от" не может быть больше "Зарплаты до"!')
        return values
