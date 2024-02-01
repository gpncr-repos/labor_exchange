"""Сценарии, работающие с таблице откликов responses"""
from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.repos import RepoResponse
from models import Job
from models import Response as ResponseForVacancy

from api.schemas.response_schema import SResponseForJob


async def respond_to_vacancy(
    db: AsyncSession,
    vacancy_response_schema: SResponseForJob,
    ):
    """Записывает в базу отклик на указанную вакансию"""
    repo_resp = RepoResponse(db)
    apply_for_vacancy = ResponseForVacancy(
        user_id=vacancy_response_schema.user_id,
        job_id=vacancy_response_schema.job_id,
        message=vacancy_response_schema.message,
    )
    repo_resp.add(apply_for_vacancy)

async def response_job(
    db: AsyncSession,
    job_id: int,
    ):
    """Записывает в базу отклик на указанную вакансию

    По ТЗ требовалась реализация метода с такой сигнатурой.
    Но странно фиксировать отклики, не указывая, кто откликнулся"""
    repo_resp = RepoResponse(db)
    apply_for_vacancy = ResponseForVacancy(
        user_id=None,
        job_id=job_id,
        message=None,
    )
    repo_resp.add(apply_for_vacancy)

async def get_responses_by_job_id(
        db: AsyncSession,
        job_id: int,
    ) -> list[Job]: # TODO: list or tuple?
    """Возвращает отклики на заданную вакансию"""
    repo_resp = RepoResponse(db)
    result = await repo_resp.get_responses_by_job_id(job_id)
    return result
