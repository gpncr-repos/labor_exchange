from fastapi import APIRouter, Depends, HTTPException, status, Body
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse

from api.schemas.job_schemas import SJob, SRemoveJobReport, SimpleTextReport
from applications.dependencies import get_current_user, get_db
from applications.queries.job_queries import create_job, convert_job_schema_to_do, delete_job
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
        if result.errors:
            return JSONResponse(
                content=str(result.errors),
                status_code=status.HTTP_400_BAD_REQUEST,
            )
        else:
            msg = "Вакансия %s добавлена с идентификатором %s" % (job_schema.title, str(result.result))
            return SimpleTextReport(message=msg)
    else:
        msg = "Пользователю %s, не являющемуся компанией, не разрешено создавать вакансии" % current_user.name
        raise HTTPException(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
            detail=msg)

@router.delete(
    "/{job_id}",
    summary="Удаление вакансии",
    description="Удаляет вакансию по идентификатору",
    response_model=SRemoveJobReport,
)
async def delete_job(
        job_id: int,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user),
    ):
    if current_user.is_company:
        res = await delete_job(db, job_id, current_user.id)
        if res.errors:
            return JSONResponse(
                content=str(res.errors),
                status_code=status.HTTP_400_BAD_REQUEST,
            )
        else:
            return SRemoveJobReport(message=str(res.result))
    else:
        msg = "Пользователь %s не является работодателем, поэтому не может удалять вакансии" % current_user.name
        return JSONResponse(
            content=str(msg),
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
        )
