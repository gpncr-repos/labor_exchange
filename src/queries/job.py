from typing import List

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy_mock import AsyncSession
from starlette import status

from models import Job
from schemas.job import JobSchema


async def create_job(db: AsyncSession, job_schema: JobSchema):
    new_job = Job(
        user_id=job_schema.user_id,
        title=job_schema.title,
        description=job_schema.description,
        salary_from=job_schema.salary_from,
        salary_to=job_schema.salary_to,
        is_active=job_schema.is_active,
        created_at=job_schema.created_at
    )
    db.add(new_job)
    await db.commit()
    await db.refresh(new_job)
    return new_job


async def get_all_jobs(db: AsyncSession, limit: int = 100, skip: int = 0) -> List[Job]:
    request = select(Job).limit(limit).offset(skip)
    result = await db.execute(request)
    list_of_jobs = result.fetchall()
    return list_of_jobs


async def get_job_by_id(db: AsyncSession, job_id: str) -> JobSchema:
    request = select(Job).where(Job.id == int(job_id))
    result = await db.execute(request)
    job = result.scalars().first()
    if job is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="job not found")
    return job
