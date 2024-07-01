import datetime
from typing import Optional
from pydantic import BaseModel, field_validator, ConfigDict


class JobSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: Optional[int] = None
    user_id: int
    title: str
    description: str
    salary_from: Optional[float]
    salary_to: Optional[float]
    is_active: bool
    created_at: datetime.datetime


class JobUpdateSchema(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    salary_from: Optional[float] = None
    salary_to: Optional[float] = None
    is_active: Optional[bool] = None

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


class JobInSchema(BaseModel):
    title: str
    description: str
    salary_from: Optional[float]
    salary_to: Optional[float]
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
