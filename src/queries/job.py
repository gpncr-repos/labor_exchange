from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import Job
from schemas import JobCreateSchema, JobUpdateSchema


async def create(db: AsyncSession, job_schema: JobCreateSchema, creator_id: int) -> Job:
    job = Job(
        title=job_schema.title,
        description=job_schema.description,
        salary_from=job_schema.salary_from,
        salary_to=job_schema.salary_to,
        is_active=job_schema.is_active,
        user_id=creator_id
    )
    db.add(job)
    await db.commit()
    await db.refresh(job)
    return job


async def get_all(db: AsyncSession, limit: int = 100, skip: int = 0) -> List[Job]:
    query = select(Job).limit(limit).offset(skip)
    res = await db.execute(query)
    return res.scalars().all()


async def get_by_id(db: AsyncSession, id: int) -> Optional[Job]:
    query = select(Job).where(Job.id == id)
    res = await db.execute(query)
    return res.scalars().first()


async def update(db: AsyncSession, job: Job, update_schema: JobUpdateSchema) -> Job:
    update_dict = update_schema.dict(exclude_none=True)
    for k, v in update_dict.items():
        setattr(job, k, v)

    db.add(job)
    await db.commit()
    await db.refresh(job)
    return job


async def delete(db: AsyncSession, job: Job) -> None:
    await db.delete(job)
    await db.commit()
