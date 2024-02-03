"""Сценарии, работающие с таблице откликов responses"""
from sqlalchemy.ext.asyncio import AsyncSession

from applications.command import CommandResult
from infrastructure.repos import RepoResponse, get_resps_by_job_id, RepoJob
from models import Job
from models import Response as ResponseForVacancy

from api.schemas.response_schema import SResponseForJob


async def respond_to_vacancy(
    db: AsyncSession,
    vacancy_response_schema: SResponseForJob,
    ):
    """Записывает в базу отклик на указанную вакансию"""
    try:
        repo_resp = RepoResponse(db)
        repo_job = RepoJob(db)
        job = await repo_job.get_by_id(vacancy_response_schema.job_id)
        if not job:
            msg = "Вакансия с идентификатором %s не найдена в базе" % vacancy_response_schema.job_id
            return CommandResult.fail(message=msg)

        apply_for_vacancy = ResponseForVacancy(
            user_id=vacancy_response_schema.user_id,
            job_id=vacancy_response_schema.job_id,
            message=vacancy_response_schema.message,
        )
        # db.add(apply_for_vacancy)
        # await db.commit()
        # await db.refresh(apply_for_vacancy)
        # return apply_for_vacancy.id
        await repo_resp.add(apply_for_vacancy)
    except Exception as e:
        msg = "Ошибка при создании отклика на вакансию"
        return CommandResult.fail(message=msg, exception=str(e))

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
    # repo_resp = RepoResponse(db)
    # result = await repo_resp.get_responses_by_job_id(job_id)
    # return result
    res = await get_resps_by_job_id(db, job_id)
    return res
