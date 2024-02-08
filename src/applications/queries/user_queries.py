import fastapi
from pydantic import EmailStr

from api.schemas.response_schema import SResponseForJob
from domain.dm_schemas import DMUser, DMResponse
from infrastructure.repos import RepoUser, RepoResponse, RepoJob
from models import User, Response
from sqlalchemy.ext.asyncio import AsyncSession


async def update_current_user(
        id: int,
        user: DMUser,
        db: AsyncSession,
        current_user_mail: str,
) -> DMUser:
    """Меняет параметры пользователя на переданные по запросу пользователя"""
    repo_user = RepoUser(db)
    old_user = await repo_user.get_by_id(id)

    if old_user is None or old_user.email != current_user_mail:
        msg = "Пользователь не найден или пытается редактировать не свои данные"
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_400_BAD_REQUEST,
            detail=msg,
        )

    old_user.name = user.name if user.name is not None else old_user.name
    old_user.email = user.email if user.email is not None else old_user.email
    old_user.is_company = user.is_company if user.is_company is not None else old_user.is_company

    result = await repo_user.update(old_user)
    return result


async def get_by_email(db: AsyncSession, email: EmailStr) -> DMUser:
    repo_user = RepoUser(db)
    res = await repo_user.get_by_email(email)
    return res


async def respond_to_vacancy(
        db: AsyncSession,
        vacancy_response_schema: SResponseForJob,
) -> DMResponse:
    """
    Записывает в базу отклик на указанную вакансию
    """
    repo_resp = RepoResponse(db)
    repo_job = RepoJob(db)
    job = await repo_job.get_by_id(vacancy_response_schema.job_id)

    if not job:
        msg = "Вакансия с идентификатором %s не найдена в базе" % vacancy_response_schema.job_id
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_400_BAD_REQUEST,
            detail=msg,
        )

    apply_for_vacancy = DMResponse(
        user_id=vacancy_response_schema.user_id,
        job_id=vacancy_response_schema.job_id,
        message=vacancy_response_schema.message,
    )
    new_resp = await repo_resp.add(apply_for_vacancy)
    return new_resp
