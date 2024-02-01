from fastapi import APIRouter, Depends, HTTPException, status, Body
from sqlalchemy.ext.asyncio import AsyncSession

from api.schemas.job_schemas import SJob
from applications.dependencies import get_current_user, get_db
from applications.queries.job_queries import create_job, convert_job_schema_to_do
from infrastructure.repos import RepoJob
from models import User

router = APIRouter(
    prefix="/job",
    tags=["vacancies"],
)

@router.post("", summary="Разместить вакансию") # TODO: add response_model
async def place_job(
        job_in_schema: SJob = Body(description="Характеристики вакансии"),
        # job_schema: SJob,   # TODO: solve a problem with this parameter
        current_user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db),
    ):
    if current_user.is_company:
        job_schema = convert_job_schema_to_do(current_user.id, job_in_schema)
        result = await create_job(db, job_schema)
    else:
        msg = "Пользователю %s, не являющемуся компанией, не разрешено создавать вакансии" % current_user.name
        raise HTTPException(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
            detail=msg)
