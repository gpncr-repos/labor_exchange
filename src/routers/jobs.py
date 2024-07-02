from typing import List, Optional, Annotated
from fastapi import APIRouter, Depends, HTTPException, status, Query
from schemas import JobSchema, JobInSchema, JobUpdateSchema
from dependencies import get_db, get_current_user
from sqlalchemy.ext.asyncio import AsyncSession
from queries import user as user_queries
from queries import jobs as jobs_queries
from queries import responses as responses_queries
from models import User


router = APIRouter(prefix="/jobs", tags=["jobs"])


@router.get("", response_model=List[JobSchema])
async def read_jobs(
    db: AsyncSession = Depends(get_db),
    filter_by_salary: jobs_queries.FilterBySalary = Query(description="Фильтр по зарплате"),
    filter_by_activeness: jobs_queries.FilterByActiveness = Query(description="Фильтр по активности"),
    order_by: jobs_queries.OrderBy = Query(description="Сортировка по времени"),
    limit: int = 100,
    skip: int = 0,
    salary: float = 0):
    item_id = 1
    return await jobs_queries.get_all_jobs(db=db, filter_by_salary=filter_by_salary, filter_by_activeness=filter_by_activeness, order_by=order_by, limit=limit, skip=skip, salary=salary)

@router.get("/{id}", response_model=List[JobSchema])
async def read_my_jobs(
    id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)):
    id = current_user.id
    if current_user.is_company is False:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Вы соискатель. Вакансии создаются компаниями")

    return await jobs_queries.get_all_jobs_by_user_id(db=db, user_id=current_user.id)


@router.post("", response_model=JobSchema)
async def create_job(
    job: JobInSchema,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)):

    if current_user.is_company is False:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Вы соискатель. Вакансии создаются компаниям")

    new_job = await jobs_queries.create_job(db=db, job_schema=job, user_id=current_user.id)
    return JobSchema.from_orm(new_job)


@router.put("", response_model=JobSchema)
async def update_job(
    id: int,
    job: JobUpdateSchema,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)):

    old_job = await jobs_queries.get_job_by_id(db=db, job_id=id)

    if old_job is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Вакансия не найдена")
    if old_job.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Это не ваша вакансия")

    old_job.title = job.title if job.title is not None else old_job.title
    old_job.description = job.description if job.description is not None else old_job.description
    old_job.salary_from = job.salary_from if job.salary_from is not None else old_job.salary_from
    old_job.salary_to = job.salary_to if job.salary_to is not None else old_job.salary_to
    old_job.is_active = job.is_active if job.is_active is not None else old_job.is_active

    new_job = await user_queries.update(db=db, user=old_job)

    return JobSchema.from_orm(new_job)


@router.delete("", response_model=JobSchema)
async def delete_job(
    id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)):

    old_job = await jobs_queries.get_job_by_id(db=db, job_id=id)

    if old_job is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Вакансия не найдена")
    if old_job.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Это не ваша вакансия")
    old_responses = await responses_queries.get_response_by_job_id(db=db, job_id=id)
    await responses_queries.delete_some_responses(db=db, responses=old_responses)
    new_job = await jobs_queries.delete_job(db=db, job=old_job)
    return JobSchema.from_orm(new_job)
