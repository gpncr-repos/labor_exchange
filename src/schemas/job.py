import datetime
from decimal import Decimal
from typing import Optional
from pydantic import BaseModel, condecimal, validator, root_validator


class _JobBaseSchema(BaseModel):
    title: str
    description: str
    salary_from: Decimal
    salary_to: Decimal
    is_active: bool


class JobSchema(_JobBaseSchema):
    id: int
    created_at: datetime.datetime

    class Config:
        orm_mode = True


class JobCreateSchema(_JobBaseSchema):
    salary_from: condecimal(gt=Decimal(0), decimal_places=2)
    salary_to: condecimal(gt=Decimal(0), decimal_places=2)
    is_active: bool = True

    @validator("salary_to")
    def salary_range(cls, v, values):
        if "salary_from" in values and v < values["salary_from"]:
            raise ValueError("salary_to cannot be less than salary_from!")
        return v


class JobUpdateSchema(_JobBaseSchema):
    title: Optional[str]
    description: Optional[str]
    salary_from: Optional[condecimal(gt=Decimal(0), decimal_places=2)]
    salary_to: Optional[condecimal(gt=Decimal(0), decimal_places=2)]
    is_active: Optional[bool]

    @root_validator
    def salary_check(cls, values):
        s_from = values.get("salary_from")
        s_to = values.get("salary_to")
        if s_from and not s_to or s_to and not s_from:
            raise ValueError("To update salary range specify both salary_from and salary_to")
        if s_from and s_to and s_to < s_from:
            raise ValueError("salary_to cannot be less than salary_from!")

        return values
