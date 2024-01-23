from pydantic import BaseModel


class JobSchema(BaseModel):
    class Config:
        orm_mode = True

    id: int | None = None
    user_id: int
    title: str | None = None
    description: str = None
    salary_from: float | None = None
    salary_to: float | None = None
    is_active: bool = True
