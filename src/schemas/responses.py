from typing import Optional
from pydantic import BaseModel, ConfigDict


class ResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: Optional[int] = None
    user_id: int
    job_id: int
    message: str


class ResponseUpdateSchema(BaseModel):
    job_id: Optional[int] = None
    message: Optional[str] = None

