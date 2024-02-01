from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from applications.dependencies import get_db
from applications.queries.response_query import get_responses_by_job_id

router = APIRouter(
    prefix="/response",
    tags=["отклики",]
)

@router.get(
    "/{job_id}",
    summary="Получить список откликов на выбранную вакансию",
    ) # TODO: add, response_model=)
async def get_job_responses(
    job_id: int,
    db: AsyncSession = Depends(get_db),
    ):
    # """Возвращает отклики на заданную вакансию"""
    result = await get_responses_by_job_id(db, job_id)
    return result
