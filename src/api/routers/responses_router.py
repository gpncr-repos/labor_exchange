from typing import List

from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.schemas.response_schema import SResponseForJob
from applications.dependencies import get_db
from infrastructure.repos import RepoResponse

router = APIRouter(
    prefix="/response",
    tags=["отклики",]
)

@router.get(
    "/{job_id}",
    summary="Получение списка откликов на выбранную вакансию",
    response_model=List[SResponseForJob],
)
async def get_job_responses(
    job_id: int,
    db: AsyncSession = Depends(get_db),
    ):
    """
    Возвращает отклики на заданную вакансию

    :param job_id: int идентификатор вакансии, отклики на которую запрашиваются
    :param db: AsyncSession объект сессия для работы с базой данных
    :returns: список записей с их полями и значениями полей
    :rtype: List[SResponseForJob]
    """
    repo_resp = RepoResponse(db)
    orm_objs = await repo_resp.get_resps_by_job_id(job_id)
    result = [SResponseForJob.from_orm(orm_obj) for orm_obj in orm_objs]
    return result
