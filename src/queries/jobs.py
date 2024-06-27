import datetime

from models import Job
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Sequence


async def get_all_jobs(db: AsyncSession, limit: int = 100, skip: int = 0) -> Sequence[Job]:
    query = select(Job).limit(limit).offset(skip)
    res = await db.execute(query)
    return res.scalars().all()


async def get_job_by_id(db: AsyncSession, job_id: int) -> Optional[Job]:
    query = select(Job).where(Job.id == job_id).limit(1)
    res = await db.execute(query)
    return res.scalars().first()


async def get_all_jobs_by_min_salary(db: AsyncSession, limit: int = 100, salary: int = 0) -> Sequence[Job]:
    query = select(Job).where(Job.salary_from == salary).limit(limit)
    res = await db.execute(query)
    return res.scalars().all()


async def get_all_jobs_by_max_salary(db: AsyncSession, limit: int = 100, salary: int = 0) -> Sequence[Job]:
    query = select(Job).where(Job.salary_to == salary).limit(limit)
    res = await db.execute(query)
    return res.scalars().all()


async def get_active_jobs(db: AsyncSession, limit: int = 100) -> Sequence[Job]:
    query = select(Job).where(Job.is_active == True).limit(limit)
    res = await db.execute(query)
    return res.scalars().all()


async def get_recent_jobs(db: AsyncSession, time: datetime.datetime = (1, 0, 0, 0, 0, 0, 0, None), limit: int = 100) \
        -> Sequence[Job]:
    query = select(Job).where(datetime.datetime.today()-Job.created_at <= time).limit(limit)
    res = await db.execute(query)
    return res.scalars().all()


async def create_job(db: AsyncSession, job_schema: Job) -> Job:
    pass
    job = Job(
        id=job_schema.id,
        user_id=job_schema.user_id,
        title=job_schema.title,
        description=job_schema.description,
        salary_from=job_schema.salary_from,
        salary_to=job_schema.salary_to,
        is_active=job_schema.is_active,
        created_at=job_schema.salary_from
    )
    db.add(job)
    await db.commit()
    await db.refresh(job)
    return job
