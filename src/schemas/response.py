from typing import Optional

from pydantic import BaseModel


class ResponseJobSchema(BaseModel):
    user_id: int
    message: Optional[str]

    class Config:
        orm_mode = True


class ResponseInSchema(BaseModel):
    user_id: int
    job_id: int
    message: Optional[str] = None
