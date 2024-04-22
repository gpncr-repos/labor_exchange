from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from schemas.job import JobSchema, JobInSchema, JobUpdateSchema
from dependencies import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from queries import job as job_queries

router = APIRouter(prefix="/jobs", tags=["jobs"])


@router.get("", response_model=List[JobSchema])
async def read_jobs(
        db: AsyncSession = Depends(get_db),
        limit: int = 100,
        skip: int = 0):
    return await job_queries.get_all_jobs(db=db, limit=limit, skip=skip)


@router.post("", response_model=JobSchema)
async def create_job(job: JobInSchema, db: AsyncSession = Depends(get_db)):
    job = await job_queries.create_job(db=db, job_schema=job)
    return JobSchema.from_orm(job)


@router.put("", response_model=JobSchema)
async def update_job(
        id: int,
        job: JobUpdateSchema,
        db: AsyncSession = Depends(get_db)):
    old_job = await job_queries.get_job_by_id(db=db, id=id)

    if old_job is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Вакансия не найдена")

    old_job.title = job.title if job.title is not None else old_job.title
    old_job.description = job.description if job.description is not None else old_job.description
    old_job.salary_from = job.salary_from if job.salary_from is not None else old_job.salary_from
    old_job.salary_to = job.salary_to if job.salary_to is not None else old_job.salary_to
    old_job.is_active = job.is_active if job.is_active is not None else old_job.is_active

    new_job = await job_queries.update_job(db=db, job=old_job)

    return JobSchema.from_orm(new_job)
