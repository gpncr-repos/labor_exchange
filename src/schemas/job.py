import datetime
import decimal
from typing import Optional
from pydantic import BaseModel, condecimal, validator


class JobSchema(BaseModel):
    id: Optional[int] = None
    user_id: Optional[int] = None
    title: str
    description: str
    salary_from: decimal
    salary_to: decimal
    is_active: bool
    created_at: datetime.datetime

    class Config:
        orm_mode = True


class JobUpdateSchema(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    salary_from: Optional[decimal] = None
    salary_to: Optional[decimal] = None
    is_active: Optional[bool] = None


class JobInSchema(BaseModel):
    title: str
    description: str
    salary_from: condecimal(gt=0)
    salary_to: condecimal(gt=0)
    is_active: bool

    @validator("salary_from", "salary_to")
    def validate_one_field_using_the_others(cls, values):
        check_salary_from = values["salary_from"]
        check_salary_to = values["salary_to"]
        if check_salary_from > check_salary_to:
            raise ValueError("Некорректно введен уровень ЗП - значение <от> выше значения <до>")
        return True
