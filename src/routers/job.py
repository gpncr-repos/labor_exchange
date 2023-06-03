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
    Create a new job with the provided details.

    - **job_in**: Details of the job to be created.
    - **db**: Database session dependency.
    - **current_user**: Current authenticated user dependency.
    - **Returns**: Created job details.
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
    Get a list of jobs.

    - **db**: Database session dependency.
    - **limit**: Maximum number of jobs to retrieve (default: 100).
    - **skip**: Number of jobs to skip (default: 0).
    - **Returns**: List of jobs.
    """

    jobs = await job_service.get_all_jobs(db=db, limit=limit, skip=skip)
    return jobs


@router.get('/{job_id}', response_model=JobSchema)
async def get_job_by_id(
        job_id: int,
        db: AsyncSession = Depends(get_db)
):
    """
    Get a job by its ID.

    - **job_id**: ID of the job to retrieve.
    - **db**: Database session dependency.
    - **Returns**: Job details.
    """

    job = await job_service.get_job_by_id(db=db, job_id=job_id)
    if job is None:
        raise HTTPException(status_code=404, detail="Работа не найдена")

    return JobSchema.from_orm(job)
