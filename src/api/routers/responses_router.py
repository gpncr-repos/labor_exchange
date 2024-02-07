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
    summary="Получить список откликов на выбранную вакансию",
    response_model=List[SResponseForJob],
)
async def get_job_responses(
    job_id: int,
    db: AsyncSession = Depends(get_db),
    ):
    # """Возвращает отклики на заданную вакансию"""
    repo_resp = RepoResponse(db)
    orm_objs = await repo_resp.get_resps_by_job_id(db, job_id)
    result = [SResponseForJob.from_orm(orm_obj) for orm_obj in orm_objs]
    return result
