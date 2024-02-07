from typing import List

from fastapi import APIRouter, Depends, HTTPException, status, Body
from sqlalchemy.ext.asyncio import AsyncSession

from api.schemas.job_schemas import SJob, SRemoveJobReport, SimpleTextReport
from applications.dependencies import get_current_user, get_db
from applications.queries.job_queries import create_job, convert_job_schema_to_do, get_job_by_id, \
    delete_job_by_id, update_job
from domain.do_schemas import DOUser, DOJob, DOJobEdit
from infrastructure.repos import RepoJob
from models import User

router = APIRouter(
    prefix="/job",
    tags=["vacancies"],
)

@router.post("",
             summary="Разместить вакансию",
             # response_model=SimpleTextReport) # TODO: add response_model,
             response_model=SJob) # TODO: add response_model
async def place_job(
        job_in_schema: SJob = Body(description="Характеристики вакансии"),
        current_user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db),
    ):
    if current_user.is_company:
        job_schema = convert_job_schema_to_do(current_user.id, job_in_schema)
        result = await create_job(db, job_schema)
        # return SimpleTextReport(id=result.result, message=msg)
        return SJob.from_orm(result)
    else:
        msg = "Пользователю %s, не являющемуся компанией, не разрешено создавать вакансии" % current_user.name
        raise HTTPException(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
            detail=msg)

@router.get("/jobs",
            summary="Получние списка вакансий",
            response_model=List[SJob],
            )
async def read_vacancies(
        db: AsyncSession = Depends(get_db),
    ):
    repo_job = RepoJob(db)
    orm_objs = await repo_job.get_all()
    result = [SJob.from_orm(orm_obj) for orm_obj in orm_objs]
    return result


@router.put("/{job_id}",
            summary="Редактирование вакансии",
            response_model=SJob,
            )
async def edit_job(
        job_id: int,
        job_in_schema: SJob,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user),
    ):
    job_schema = DOJobEdit(
        title=job_in_schema.title,
        description=job_in_schema.description,
        salary_from=job_in_schema.salary_from,
        salary_to=job_in_schema.salary_to,
        is_active=job_in_schema.is_active,
    )
    updated_job = await update_job(job_id, db, job_schema, current_user.id)
    return SJob.from_orm(updated_job)

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
        try:
            res = await delete_job_by_id(db, job_id, current_user.id)
            return SRemoveJobReport(id=job_id, message="Вакансия %s удалена" % job_id)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
    #     if res.errors:
    #         return JSONResponse(
    #             content=str(res.errors),
    #             status_code=status.HTTP_400_BAD_REQUEST,
    #         )
    #     else:
    #         return SRemoveJobReport(id=job_id, message=str(res.result))
    # else:
    #     msg = "Пользователь %s не является работодателем, поэтому не может удалять вакансии" % current_user.name
    #     return JSONResponse(
    #         content=str(msg),
    #         status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
    #     )
