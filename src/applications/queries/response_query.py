"""Сценарии, работающие с таблице откликов responses"""
from sqlalchemy.ext.asyncio import AsyncSession

from applications.command import CommandResult
from domain.do_schemas import DOJob, DOResponse
from infrastructure.repos import RepoResponse, RepoJob
from models import Job
from models import Response as ResponseForVacancy

from api.schemas.response_schema import SResponseForJob


async def respond_to_vacancy(
    db: AsyncSession,
    vacancy_response_schema: DOResponse,
    ) -> CommandResult:
    """Записывает в базу отклик на указанную вакансию"""
    try:
        repo_resp = RepoResponse(db)
        repo_job = RepoJob(db)
        job = await repo_job.get_by_id(vacancy_response_schema.job_id)
        if not job:
            msg = "Вакансия с идентификатором %s не найдена в базе" % vacancy_response_schema.job_id
            return CommandResult.fail(message=msg)

        apply_for_vacancy = DOResponse(
            user_id=vacancy_response_schema.user_id,
            job_id=vacancy_response_schema.job_id,
            message=vacancy_response_schema.message,
        )
        new_resp = await repo_resp.add(apply_for_vacancy)
        return CommandResult.success(result=new_resp)

    except Exception as e:
        msg = "Ошибка при создании отклика на вакансию"
        return CommandResult.fail(message=msg, exception=str(e))

# async def response_job(
#     db: AsyncSession,
#     job_id: int,
#     ):
#     """Записывает в базу отклик на указанную вакансию
#
#     По ТЗ требовалась реализация метода с такой сигнатурой.
#     Но странно фиксировать отклики, не указывая, кто откликнулся"""
#     repo_resp = RepoResponse(db)
#     apply_for_vacancy = DOResponse(
#         user_id=None,
#         job_id=job_id,
#         message=None,
#     )
#     repo_resp.add(apply_for_vacancy)

async def get_responses_by_job_id(
        db: AsyncSession,
        job_id: int,
    ) -> list[DOJob]: # TODO: list or tuple?
    """Возвращает отклики на заданную вакансию"""
    repo_resp = RepoResponse(db)
    res = await repo_resp.get_resps_by_job_id(db, job_id)
    return res
