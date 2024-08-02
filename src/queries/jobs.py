from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import Job
from schemas import JobSchema, JobtoSchema


async def get_all(db: AsyncSession, limit: int = 100, skip: int = 0) -> List[JobSchema]:
    query = select(Job).limit(limit).offset(skip)
    res = await db.execute(query)
    return res.scalars().all()


async def get_by_id(db: AsyncSession, id: int) -> JobSchema:
    query = select(Job).where(Job.id == id)
    res = await db.execute(query)
    return res.scalars().first()


async def create(db: AsyncSession, job_schema: JobtoSchema, curent_user_id) -> Job:
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


async def update(db: AsyncSession, job: Job) -> Job:
    db.add(job)
    await db.commit()
    await db.refresh(job)
    return job


async def delete(db: AsyncSession, job: Job) -> JobSchema:
    id = job.id
    await db.delete(job)
    await db.commit()
    res = await get_by_id(db=db, id=id)
    return res
