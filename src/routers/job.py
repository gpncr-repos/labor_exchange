from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from queries import job as job_service
from dependencies import get_db, get_current_user
from models import User
from schemas import JobSchema, JobInSchema

router = APIRouter(prefix='/jobs', tags=['jobs'])


@router.post('', response_model=JobSchema)
async def create_job(
        job_in: JobInSchema,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    """
            обрабатывает HTTP POST-запросы на пути /jobs,
            принимает модель данных JobInSchema,
            создает "работу" в базе данных с использованием сервиса job_service,
            возвращает созданную "работу" в формате JobSchema
    """

    created_job = await job_service.create_job(db=db, job_schema=job_in, current_user=current_user)
    return JobSchema.from_orm(created_job)


@router.get('', response_model=List[JobSchema])
async def get_jobs(
        db: AsyncSession = Depends(get_db),
        limit: int = 100,
        skip: int = 0
):
    """
            Обрабатывает HTTP GET-запросы на пути /jobs,
            возвращает список работ в формате List[JobSchema].
    """

    return job_service.get_all_jobs(db=db, limit=limit, skip=skip)


@router.get('/{job_id}', response_model=JobSchema)
async def get_job_by_id(
        job_id: int,
        db: AsyncSession = Depends(get_db)
):
    """
            Обрабатывает HTTP GET-запросы на пути /jobs/{job_id},
            возвращает работу с указанным идентификатором в формате JobSchema.
    """

    job = await job_service.get_job_by_id(db=db, job_id=job_id)
    if job is None:
        raise HTTPException(status_code=404, detail="Работа не найдена")

    return JobSchema.from_orm(job)
