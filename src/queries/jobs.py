from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import Job
from schemas import JobCreateSchema, JobSchema


async def get_all(db: AsyncSession, limit: int = 100, skip: int = 0) -> List[Job]:
    query = select(Job).limit(limit).offset(skip)
    res = await db.execute(query)
    return res.scalars().all()


async def get_by_id(db: AsyncSession, job_id: int) -> Optional[Job]:
    query = select(Job).where(Job.id == job_id)
    res = await db.execute(query)
    return res.scalars().first()


async def create(db: AsyncSession, job_schema: JobCreateSchema, curent_user_id) -> Optional[Job]:
    job = Job(
        user_id=curent_user_id,
        title=job_schema.title,
        discription=job_schema.discription,
        salary_from=job_schema.salary_from,
        salary_to=job_schema.salary_to,
        is_active=job_schema.is_active,
    )
    db.add(job)
    await db.commit()
    await db.refresh(job)
    return job


async def update(db: AsyncSession, update_job: JobSchema) -> Optional[Job]:
    db.add(update_job)
    await db.commit()
    await db.refresh(update_job)
    updated_job = await get_by_id(db=db, job_id=update_job.id)
    return updated_job


async def delete(db: AsyncSession, delete_job: JobSchema) -> Optional[Job]:
    id = delete_job.id
    await db.delete(delete_job)
    await db.commit()
    res = await get_by_id(db=db, job_id=id)
    return res
