from typing import Optional
from pydantic import BaseModel, Field, validator


def validate_salary_not_negative(salary: int):
    if salary is not None and salary <= 0:
        raise ValueError("Зарплата должна быть больше нуля")
    return salary


def validate_salary_to_not_less_than_from(salary, values, **kwargs):
    if salary is not None and 'salary_from' in values and values["salary_from"] is not None:
        if salary < values["salary_from"]:
            raise ValueError("Верхняя граница зарплаты не может быть меньше нижней границы!")
    return salary


class JobInSchema(BaseModel):
    title: str
    description: Optional[str]
    salary_from: Optional[float]
    salary_to: Optional[float]

    @validator('salary_from')
    def validate_salary_from(cls, salary):
        return validate_salary_not_negative(salary)

    @validator('salary_to')
    def validate_salary_to(cls, salary, values):
        return validate_salary_to_not_less_than_from(salary, values)

    class Config:
        schema_extra = {
            "example": {
                "title": "Ведущий разработчик Python в ГПН ЦР",
                "description": "Требуется разработчик с опытом 10 лет",
                "salary_from": 300000,
                "salary_to": 400000,
            }
        }
        validate_assignment = True


class JobSchema(BaseModel):
    user_id: int
    id: Optional[int] = None
    title: str
    description: Optional[str]
    is_active: bool
    salary_from: Optional[float]
    salary_to: Optional[float]

    @validator('salary_from')
    def validate_salary_from(cls, salary):
        return validate_salary_not_negative(salary)

    @validator('salary_to')
    def validate_salary_to(cls, salary, values):
        return validate_salary_to_not_less_than_from(salary, values)

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
        validate_assignment = True
