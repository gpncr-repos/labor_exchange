import datetime
from typing import Optional
from pydantic import BaseModel, field_validator, ConfigDict


class JobSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: Optional[int] = None
    user_id: int
    title: str
    description: str
    salary_from: int
    salary_to: int
    is_active: bool
    created_at: datetime.datetime


class JobInSchema(BaseModel):
    title: str
    description: str
    salary_from: int
    salary_to: int
    is_active: bool = False

    @field_validator("salary_from")
    def min_salary_match(cls, v, **kwargs) -> str:
        if v <= 0:
            raise ValueError("Минимальная зарплата должна быть положительной")
        return v

    @field_validator("salary_to")
    def max_salary_match(cls, v, values, **kwargs) -> str:
        if v <= 0 or 'salary_from' in values.data and v < values.data["salary_from"]:
            raise ValueError("Максимальная зарплата должна быть положительной и больше минимальной зарплаты")
        return v
