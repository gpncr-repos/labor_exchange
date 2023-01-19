from typing import Optional

from pydantic.main import BaseModel


class ResponseInSchema(BaseModel):
    user_id: int
    job_id: int
    message: Optional[str]


class ResponseJobSchema(BaseModel):
    user_id: int
    message: Optional[str]

    class Config:
        orm_mode = True
