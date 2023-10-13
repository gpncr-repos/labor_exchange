from typing import Optional

from pydantic import BaseModel, ConfigDict


class ResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    user_id: int
    job_id: int
    message: Optional[str] = None


class ResponseInSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    job_id: int
    message: Optional[str] = None
