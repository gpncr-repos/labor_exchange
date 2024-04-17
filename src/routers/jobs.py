from typing import List

from fastapi import APIRouter, Body, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import get_current_employer, get_db
from models import User
from queries import jobs as jobs_queries
from schemas import JobInSchema, JobSchema, JobUpdateSchema

router = APIRouter(prefix="/jobs", tags=["jobs"])


@router.get("", response_model=List[JobSchema])
async def get_jobs_view(
    db: AsyncSession = Depends(get_db), limit: int = 100, skip: int = 0
):
    if limit < 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="limit < 0")
    if skip < 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="skip < 0")

    return await jobs_queries.get_all_jobs(db=db, limit=limit, skip=skip)


@router.get("/{job_id}", response_model=JobSchema)
async def get_job_by_id_view(
    db: AsyncSession = Depends(get_db), job_id: int = Query(...)
):
    res = await jobs_queries.get_job_by_id(db=db, job_id=job_id)
    if res is not None:
        return res
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Вакансия не найдена"
        )


@router.post("", response_model=JobSchema)
async def create_job(
    db: AsyncSession = Depends(get_db),
    new_job: JobInSchema = Body(...),
    current_employer: User = Depends(get_current_employer),
):
    return await jobs_queries.create_job(
        db=db, job_schema=new_job, user_id=current_employer.id
    )


@router.put("/{job_id}", response_model=JobSchema)
async def update_job_by_id(
    db: AsyncSession = Depends(get_db),
    job_id: int = Query(...),
    new_job: JobUpdateSchema = Body(...),
    current_employer: User = Depends(get_current_employer),
):

    current_job = await jobs_queries.get_job_by_id(db=db, job_id=job_id)
    if not current_job.user_id == current_employer.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Недостаточно прав для изменения вакансии",
        )

    new_salary_from = (
        current_job.salary_from if new_job.salary_from is None else new_job.salary_from
    )
    new_salary_to = (
        current_job.salary_to if new_job.salary_to is None else new_job.salary_to
    )

    if new_salary_from and new_salary_to:
        if new_salary_from > new_salary_to:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='"Зарплата от" не может быть больше "Зарплаты до"',
            )

    new_job = new_job.dict(exclude_unset=True)
    return await jobs_queries.update_job(db=db, job_id=job_id, update_data=new_job)


@router.delete("/{job_id}", response_model=JobSchema)
async def delete_job_by_id(
    db: AsyncSession = Depends(get_db),
    job_id: int = Query(...),
    current_employer: User = Depends(get_current_employer),
):

    current_job = await jobs_queries.get_job_by_id(db=db, job_id=job_id)
    if not current_job.user_id == current_employer.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Недостаточно прав для удаления вакансии",
        )

    return await jobs_queries.delete_job(db=db, job_id=job_id)
