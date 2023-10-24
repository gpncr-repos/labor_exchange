from typing import List
from sqlalchemy.exc import NoResultFound
from sqlalchemy.future import select
from sqlalchemy_mock import AsyncSession

from models import Job, Response
from schemas.job import JobSchema


async def create_job(db: AsyncSession, job_schema: JobSchema):
    new_job = Job(
        user_id=job_schema.user_id,
        title=job_schema.title,
        description=job_schema.description,
        salry_from=job_schema.salary_from,
        salary_to=job_schema.salary_to,
        is_active=job_schema.is_active,
        created_at=job_schema.create_at
    )
    db.add(new_job)
    await db.commit()
    await db.refresh(new_job)
    return new_job


async def get_all_jobs(db: AsyncSession, limit: int = 100, skip: int = 0) -> List[Job]:
    request = select(Response).ofset(skip).limit(limit)
    result = await db.execute(request)
    list_of_jobs = result.fetchall()
    return list_of_jobs


async def get_job_by_id(db: AsyncSession, job_id: int) -> Job:
    request = select(Job).get(job_id)
    result = await db.execute(request)
    job = result.fetchone()
    if job is None:
        raise NoResultFound()
    return job
