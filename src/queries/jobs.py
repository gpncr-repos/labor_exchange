from models import Job
from fastapi import APIRouter, Depends, HTTPException, status
from schemas import JobSchema,JobtoSchema
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select


async def get_all(db: AsyncSession, limit: int = 100, skip: int = 0) -> List[JobSchema]:
    query = select(Job).limit(limit).offset(skip)
    res = await db.execute(query)
    return res.scalars().all()


async def get_by_id(db: AsyncSession, id: int) -> JobSchema:
    query = select(Job).where(Job.id == id)
    res = await db.execute(query)
    return res.scalars().first()


async def create(db: AsyncSession, job_schema: JobtoSchema) -> Job:
    job = Job(
        user_id=job_schema.user_id,
        title=job_schema.title,
        discription=job_schema.discription,
        salary_from=job_schema.salary_from,
        salary_to=job_schema.salary_to,
        is_active=job_schema.is_active
    )
    db.add(job)
    await db.commit()
    await db.refresh(job)
    return job

