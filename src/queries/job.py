from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.tables import Job
from src.schemas.job import JobSchema


async def create_new_job(job_schema: JobSchema, session: AsyncSession):
    job = Job(
        user_id=job_schema.user_id,
        title=job_schema.title,
        description=job_schema.description,
        is_active=job_schema.is_active,
        salary_from=job_schema.salary_from,
        salary_to=job_schema.salary_to,
    )
    session.add(job)
    await session.commit()


async def get_all_jobs(session: AsyncSession, limit: int = 100, skip: int = 0) -> list[Job]:
    query = select(Job).limit(limit).offset(skip)
    res = await session.execute(query)
    return res.scalars().all()


async def get_job_by_id(id: int, session: AsyncSession, lock: bool = False) -> Job | None:
    query = select(Job).where(Job.id == id)
    if lock:
        query = query.with_for_update(nowait=False)
    res = await session.execute(query)
    return res.scalar()


async def update_job_by_id(session: AsyncSession, old_job: Job, new_job: JobSchema):
    old_job.id = new_job.id if new_job.id is not None else old_job.id
    old_job.title = new_job.title if new_job.title else old_job.title
    old_job.description = new_job.description if new_job.description else old_job.description
    old_job.salary_from = new_job.salary_from if new_job.salary_from is not None else old_job.salary_from
    old_job.salary_to = new_job.salary_to if new_job.salary_to is not None else old_job.salary_to
    old_job.is_active = new_job.is_active

    session.add(old_job)
    await session.commit()
