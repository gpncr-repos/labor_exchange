from typing import Optional

from pydantic import BaseModel, Field


class SResponseForJob(BaseModel):
    """Схема отклика на вакансию"""
    id: int
    user_id: int = Field(default_factory=int, title="Идентификатор пользователя-работодателя, разместившего вакансию")
    job_id: int = Field(default_factory=int, title="Идентификатор вакансии")
    message: Optional[str] = Field(default=None, title="Текст сопроводительного письма", max_length=2000)

    class Config:
        orm_mode = True
