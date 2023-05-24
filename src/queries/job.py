from typing import List, Optional

from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from models import Job, Response, User
from schemas.job import CreateJobRequest, CreateResponseRequest


async def create_job(db: AsyncSession, user_id:int, job_schema: CreateJobRequest) -> Job:
    job = Job(
        user_id=user_id,
        title=job_schema.title,
        description=job_schema.description,
        salary_from=job_schema.salary_from,
        salary_to=job_schema.salary_to,
        is_active=True,
    )
    db.add(job)
    await db.commit()
    await db.refresh(job)
    return job


async def get_job_by_id(db: AsyncSession, id: int) -> Optional[Job]:
    query = select(Job).where(Job.id == id).limit(1)
    res = await db.execute(query)
    return res.scalars().first()

async def remove_job(db: AsyncSession, id: int):
    query = delete(Job).where(Job.id == id)
    await db.execute(query)
    await db.commit()

async def update_job(db: AsyncSession, job_model: Job):
    await db.merge(job_model)
    await db.commit()
    await db.refresh(job_model)
    return job_model

async def get_all_jobs(db: AsyncSession, limit: int = 100, skip: int = 0) -> List[Job]:
    query = select(Job).limit(limit).offset(skip)
    res = await db.execute(query)
    return res.scalars().all()


async def create_response(db: AsyncSession, job_id: int, user_id:int, response_schema:CreateResponseRequest) -> Response:
    response = Response(
        user_id=user_id,
        job_id=job_id,
        message=response_schema.message,
    )
    db.add(response)
    await db.commit()
    await db.refresh(response)
    return response

async def get_response_by_job_id(db: AsyncSession, job_id: int, limit: int = 100, skip: int = 0) -> List[Response]:
    query = select(Response).where(Response.job_id == job_id).limit(limit).offset(skip)
    res = await db.execute(query)
    return res.scalars().all()