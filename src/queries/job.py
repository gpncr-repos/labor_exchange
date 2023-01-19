from models import Job
from queries.base_repository import BaseAsyncRepository
from schemas import JobInSchema
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from core.security import hash_password


# async def get_all_jobs(db: AsyncSession, limit: int = 100, skip: int = 0) -> List[Job]:
#     query = select(Job).limit(limit).offset(skip)
#     res = await db.execute(query)
#     return res.scalars().all()
#
#
# async def get_job_by_id(db: AsyncSession, id_: int) -> Optional[Job]:
#     query = select(Job).where(Job.id == id_).limit(1)
#     res = await db.execute(query)
#     return res.scalars().first()
#
#
# async def create(db: AsyncSession, user_schema: JobInSchema) -> Job:
#     job = Job(
#         **user_schema.dict(exclude_unset=True)
#     )
#     db.add(job)
#     await db.commit()
#     await db.refresh(job)
#     return job
#
#
# async def update(db: AsyncSession, job: Job) -> Job:
#     db.add(job)
#     await db.commit()
#     await db.refresh(job)
#     return job
#
#
# async def get_by_email(db: AsyncSession, email: str) -> Job:
#     query = select(Job).where(Job.email == email).limit(1)
#     res = await db.execute(query)
#     job = res.scalars().first()
#     return job


class JobRepository(BaseAsyncRepository):
    model = Job
