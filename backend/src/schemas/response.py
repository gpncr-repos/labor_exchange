from typing import Optional
from pydantic import BaseModel


class ResponseInSchema(BaseModel):
    job_id: int
    message: Optional[str]

    class Config:
        schema_extra = {
            "example": {
                "job_id": 1,
                "message": "Мне понравилась Ваша вакансия.",
            }
        }


class ResponseSchema(BaseModel):
    id: Optional[int] = None
    job_id: int
    user_id: int
    message: Optional[str]

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id": 1,
                "job_id": 1,
                "user_id": 1,
                "message": "Мне понравилась Ваша вакансия.",
            }
        }
