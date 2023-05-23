import datetime
import decimal
from typing import Optional
from pydantic import BaseModel, EmailStr, validator, constr


class JobSchema(BaseModel):
    id: Optional[str] = None
    user_id: int
    title: str
    description: str
    salary_from: decimal.Decimal
    salary_to: decimal.Decimal
    is_active: bool
    created_at: datetime.datetime

    class Config:
        orm_mode = True


class JobInSchema(BaseModel):
    title: str
    description: str
    salary_from: decimal.Decimal
    salary_to: decimal.Decimal
    is_active: bool = True
