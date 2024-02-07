from typing import Optional

from pydantic import BaseModel, Field


class SResponseForJob(BaseModel):
    """Схема отклика на вакансию"""
    user_id: int = Field(int, description="Идентификатор пользователя-работодателя, разместившего вакансию")
    job_id: int = Field(int, description="Идентификатор вакансии")
    message: Optional[str] = Field(type_=str, default=None, description="Текст сопроводительного письма", max_length=2000)
