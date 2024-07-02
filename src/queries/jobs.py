from models import Job
from schemas import JobInSchema
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc, asc
from typing import Sequence
from .utils import OrderBy, FilterBySalary, FilterByActiveness


async def get_all_jobs(db: AsyncSession, filter_by_salary: FilterBySalary, filter_by_activeness: FilterByActiveness, order_by: OrderBy, limit: int = 100, skip: int = 0, salary: float = 0) -> Sequence[Job]:
    query = select(Job)
    if filter_by_salary == FilterBySalary.MIN:
        query = query.where(Job.salary_from == salary)
    elif filter_by_salary == FilterBySalary.MAX:
        query = query.where(Job.salary_to == salary)
    if filter_by_activeness == FilterByActiveness.YES:
        query = query.where(Job.is_active == True)
    if order_by is not order_by.NO:
        if order_by == OrderBy.ASC:
            query = query.order_by(asc(Job.created_at))
        if order_by == OrderBy.DESC:
            query = query.order_by(desc(Job.created_at))
    query = query.limit(limit).offset(skip)
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


async def update(db: AsyncSession, job: Job) -> Job:
    db.add(job)
    await db.commit()
    await db.refresh(job)
    return job


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


async def delete_job(db: AsyncSession, job: Job) -> Job:
    await db.delete(job)
    await db.commit()
    return job
