from __future__ import annotations

from typing import List

from fastapi import HTTPException, status
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from models import User, Job
from schemas import JobInSchema


async def create_job(db: AsyncSession, job_schema: JobInSchema, current_user: User) -> Job | HTTPException:

    if not current_user.is_company:
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail="Только компания может создавать вакансии")

    new_job = Job(
        user_id=current_user.id,
        title=job_schema.title,
        description=job_schema.description,
        is_active=True,
        salary_from=job_schema.salary_from,
        salary_to=job_schema.salary_to
    )
    db.add(new_job)
    await db.commit()  # Сохранение изменений в базе данных
    await db.refresh(new_job)  # Обновление объекта new_job со значениями из базы данных
    return new_job


async def get_all_jobs(db: AsyncSession, limit: int = 100, skip: int = 0) -> List[Job]:
    query = select(Job).limit(limit).offset(skip)
    res = await db.execute(query)

    return res.scalars().all()


async def get_job_by_id(db: AsyncSession, job_id: int) -> Job:
    query = select(Job).where(Job.id == job_id).limit(1)
    res = await db.execute(query)

    return res.scalars().first()


async def delete_job_by_id(db: AsyncSession, job_id: int, current_user: User) -> True | HTTPException:
    job = await db.get(Job, job_id)

    if job is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Такой вакансии нет")
    if job.user_id != current_user.id:
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail="Вы не владелец этой вакансии")

    deleted_job = delete(Job).where(Job.id == job_id)
    await db.execute(deleted_job)
    await db.commit()
    return True
