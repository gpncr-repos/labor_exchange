from pydantic import BaseModel, Field, ConfigDict, field_validator, validator
from typing import Annotated
import datetime
from typing import Optional


class JobSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: Optional[int] = None
    user_id: int
    title: str
    description: str
    salary_from: float = Field(ge=0)
    salary_to: float = Field(ge=0)
    is_active: bool
    created_at: datetime.datetime

    @validator("salary_to")
    def password_match(cls, v, values, **kwargs):
        if 'salary_from' in values and v < values["salary_from"]:
            raise ValueError("Неверный диапазон зарплаты!")
        return v
#    class Config:
#        orm_mode = True


class JobInSchema(BaseModel):
    title: str
    description: str
    salary_from: float = Field(ge=0)
    salary_to: float = Field(ge=0)
    is_active: bool

    @validator("salary_to")
    def password_match(cls, v, values, **kwargs):
        if 'salary_from' in values and v < values["salary_from"]:
            raise ValueError("Неверный диапазон зарплаты!")
        return v

# TODO добавить в свагер описания полей, значения по умолчанию(примеры)
# TODO переписать @validator