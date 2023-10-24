from typing import Optional

from pydantic import BaseModel


class ResponseSchema(BaseModel):
    id: Optional[int] = None
    user_id: int
    job_id: int
    message: str

    class Config:
        orm_mode = True
