from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import get_db, get_current_user
from models import User
from schemas import (
    JobSchema, JobCreateSchema, JobUpdateSchema,
    ResponseSchema, ResponseCreateSchema
)
from queries import job as job_queries, response as response_queries

router = APIRouter(prefix="/jobs", tags=["jobs"])


@router.get("", response_model=List[JobSchema])
async def read_jobs(
    db: AsyncSession = Depends(get_db),
    limit: int = 100,
    skip: int = 0
):
    return await job_queries.get_all(db=db, limit=limit, skip=skip)


@router.post("", response_model=JobSchema)
async def create_job(
    job_schema: JobCreateSchema,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not current_user.is_company:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Создавать вакансии могут только работодатели!"
        )

    return await job_queries.create(
        db=db, job_schema=job_schema, creator_id=current_user.id
    )


@router.put("/{id}", response_model=JobSchema)
async def update_job(
    id: int,
    update_schema: JobUpdateSchema,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not current_user.is_company:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Изменять вакансии могут только работодатели!"
        )

    old_job = await job_queries.get_by_id(db=db, id=id)

    if old_job is None or old_job.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Вакансия не найдена"
        )

    return await job_queries.update(db=db, job=old_job, update_schema=update_schema)


@router.delete("/{id}", status_code=204)
async def delete_job(
    id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not current_user.is_company:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Удалять вакансии могут только работодатели!"
        )

    job = await job_queries.get_by_id(db=db, id=id)

    if job is None or job.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Вакансия не найдена"
        )

    await job_queries.delete(db=db, job=job)


@router.post("/{id}/response", response_model=ResponseSchema)
async def response_job(
    id: int,
    response_schema: ResponseCreateSchema,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.is_company:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Откликаться на вакансии могут только соискатели!"
        )

    job = await job_queries.get_by_id(db=db, id=id)

    if job is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Вакансия не найдена"
        )

    return await response_queries.response_job(
        db=db,
        job_id=job.id,
        response_schema=response_schema,
        user_id=current_user.id
    )


@router.get("/{id}/responses", response_model=List[ResponseSchema])
async def read_job_responses(
    id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not current_user.is_company:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Просматривать отклики по вакансиям могут только работодатели!"
        )

    job = await job_queries.get_by_id(db=db, id=id)

    if job is None or job.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Вакансия не найдена"
        )

    return await response_queries.get_responses_by_job_id(db=db, job_id=job.id)
