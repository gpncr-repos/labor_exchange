import datetime
import enum

from models import Job
from schemas import JobInSchema
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc, asc
from typing import Sequence


async def get_all_jobs(db: AsyncSession, limit: int = 100, skip: int = 0) -> Sequence[Job]:
    query = select(Job).limit(limit).offset(skip)
    res = await db.execute(query)
    return res.scalars().all()


async def get_job_by_id(db: AsyncSession, job_id: int) -> Optional[Job]:
    query = select(Job).where(Job.id == job_id).limit(1)
    res = await db.execute(query)
    return res.scalars().first()


async def get_all_jobs_by_user_id(db: AsyncSession, user_id: int, limit: int = 100) -> Sequence[Job]:
    query = select(Job).where(Job.user_id == user_id).limit(limit)
    res = await db.execute(query)
    return res.scalars().all()


async def get_all_jobs_by_min_salary(db: AsyncSession, limit: int = 100, salary: int = 0) -> Sequence[Job]:
    query = select(Job).where(Job.salary_from == salary).limit(limit)
    res = await db.execute(query)
    return res.scalars().all()


async def get_all_jobs_by_max_salary(db: AsyncSession, limit: int = 100, salary: int = 0) -> Sequence[Job]:
    query = select(Job).where(Job.salary_to == salary).limit(limit)
    res = await db.execute(query)
    return res.scalars().all()


class OrderBy(str, enum.Enum):
    ASC = 1
    DESC = 2


async def get_active_jobs(db: AsyncSession, order_by: Optional[OrderBy] = None, limit: int = 100) -> Sequence[Job]:
    query = select(Job).where(Job.is_active is True).limit(limit)
    if order_by is not None:
        if order_by == OrderBy.ASC:
            query = query.order_by(asc(Job.created_at))
        if order_by == OrderBy.DESC:
            query = query.order_by(desc(Job.created_at))
    res = await db.execute(query)
    return res.scalars().all()


async def create_job(db: AsyncSession, job_schema: JobInSchema, user_id: int) -> Job:
    job = Job(
        user_id=user_id,
        title=job_schema.title,
        description=job_schema.description,
        salary_from=job_schema.salary_from,
        salary_to=job_schema.salary_to,
        is_active=job_schema.is_active,
    )
    db.add(job)
    await db.commit()
    await db.refresh(job)
    return job
