"""Вспомогательные методы"""
from datetime import datetime
from api.schemas.job_schemas import SJob
from domain.dm_schemas import DMJob


def convert_job_schema_to_dm(user_id: int, job_schema: SJob) -> DMJob:
    """
    Преобразует данные для создания вакансии в объект доменной модели

    :param user_id: int идентификатор пользователя автора вакансии
    :param job_schema: SJob параметры создаваемой вакансии
    :returns: объект доменной модели вакансия
    :rtype: DMJob
    """
    result = DMJob(
        user_id=user_id,
        title=job_schema.title,
        description=job_schema.description,
        salary_from=job_schema.salary_from,
        salary_to=job_schema.salary_to,
        is_active=job_schema.is_active,
        created_at=datetime.utcnow()
    )
    return result
