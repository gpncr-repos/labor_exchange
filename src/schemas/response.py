from typing import Optional

from pydantic import BaseModel, condecimal, validator, constr


class _ResponseBaseSchema(BaseModel):
    message: Optional[str]


class ResponseSchema(_ResponseBaseSchema):
    id: int
    user_id: int

    class Config:
        orm_mode = True


class ResponseCreateSchema(_ResponseBaseSchema):
    pass
