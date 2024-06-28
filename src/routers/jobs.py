from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from schemas import JobSchema, JobInSchema
from dependencies import get_db, get_current_user
from sqlalchemy.ext.asyncio import AsyncSession
from queries import user as user_queries
from queries import jobs as jobs_queries
from models import User


router = APIRouter(prefix="/jobs", tags=["jobs"])


@router.get("/query1", response_model=List[JobSchema])
async def read_jobs(
    db: AsyncSession = Depends(get_db),
    limit: int = 100,
    skip: int = 0):
    return await jobs_queries.get_all_jobs(db=db, limit=limit, skip=skip)


@router.get("/query2", response_model=List[JobSchema])
async def read_jobs_with_min_salary(
    db: AsyncSession = Depends(get_db),
    limit: int = 100,
    salary: int = 20000):
    return await jobs_queries.get_all_jobs_by_min_salary(db=db, limit=limit, salary=salary)


@router.get("/query3", response_model=List[JobSchema])
async def read_jobs_with_max_salary(
    db: AsyncSession = Depends(get_db),
    limit: int = 100,
    salary: int = 1000000):
    return await jobs_queries.get_all_jobs_by_max_salary(db=db, limit=limit, salary=salary)


@router.get("/query4", response_model=List[JobSchema])
async def read_active_jobs(
    db: AsyncSession = Depends(get_db),
    limit: int = 100,
    order_by: Optional[jobs_queries.OrderBy] = None):
    return await jobs_queries.get_active_jobs(db=db, order_by=order_by, limit=limit)

@router.get("/query5", response_model=List[JobSchema])
async def read_my_jobs(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)):
    if current_user.is_company is False:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Вы соискатель. Вы не создавали новые места")

    return await jobs_queries.get_all_jobs_by_user_id(db=db, user_id=current_user.id)

@router.post("", response_model=JobSchema)
async def create_job(
    job: JobInSchema,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)):

    if current_user.is_company is False:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Вы соискатель. Вам нельзя нанимать сотрудников")

    new_job = await jobs_queries.create_job(db=db, job_schema=job, user_id=current_user.id)
    return JobSchema.from_orm(new_job)
