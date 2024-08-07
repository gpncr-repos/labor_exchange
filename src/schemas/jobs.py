"""Module of schemas of jobs"""

import datetime

from pydantic import BaseModel, validator


class JobSchema(BaseModel):
    """Shema of model"""

    id: int
    user_id: int
    title: str
    discription: str
    salary_from: int
    salary_to: int
    is_active: bool
    created_at: datetime.datetime

    class Config:
        orm_mode = True


class JobCreateSchema(BaseModel):
    """Shema to create model"""

    title: str
    discription: str
    salary_from: int = 0
    salary_to: int = 0
    is_active: bool = True

    class Config:
        orm_mode = True

    @validator("salary_to")
    def salary_match(cls, v, values, **kwargs):
        if v < values["salary_from"]:
            raise ValueError(
                "Некорректные данные по зарплате: зарплата сверху {} меньше чем снизу {}".format(
                    v, values["salary_from"]
                )
            )
        if values["salary_from"] < 0:
            raise ValueError(
                "Некорректные данные по зарплате: зарплата {} меньше нуля".format(
                    values["salary_from"]
                )
            )
        return v


class JobUpdateSchema(BaseModel):
    """Shema to update model"""

    title: str
    discription: str
    salary_from: int = 0
    salary_to: int = 0
    is_active: bool

    class Config:
        orm_mode = True

    @validator("salary_to")
    def salary_match(cls, v, values, **kwargs):
        if v < values["salary_from"]:
            raise ValueError(
                "Некорректные данные по зарплате: зарплата сверху {} меньше чем снизу {}".format(
                    v, values["salary_from"]
                )
            )
        if values["salary_from"] < 0:
            raise ValueError(
                "Некорректные данные по зарплате: зарплата {} меньше нуля".format(
                    values["salary_from"]
                )
            )
        return v
