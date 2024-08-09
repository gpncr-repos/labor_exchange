"""Module of schemas of responses"""

import datetime

from pydantic import BaseModel


class ResponsesSchema(BaseModel):
    """Shema of model"""

    id: int
    user_id: int
    job_id: int
    message: str
    created_at: datetime.datetime

    class Config:
        orm_mode = True


class ResponsesCreateSchema(BaseModel):
    """Schema to create"""

    message: str

    class Config:
        orm_mode = True


class ResponsesUpdateSchema(BaseModel):
    """schema to patch"""

    message: str

    class Config:
        orm_mode = True
