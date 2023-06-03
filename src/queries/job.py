from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from models import User, Job, jobs
from schemas import JobInSchema, JobSchema


async def create_job(db: AsyncSession, job_schema: JobInSchema, current_user: User):

    new_job = Job(
        user_id=current_user.id,
        title=job_schema.title,
        description=job_schema.description,
        is_active=True,
        salary_from=job_schema.salary_from,
        salary_to=job_schema.salary_to
    )
    db.add(new_job)
    await db.commit()  # Сохранение изменений в базе данных
    await db.refresh(new_job)  # Обновление объекта new_job со значениями из базы данных
    return new_job


async def get_all_jobs(db: AsyncSession, limit: int = 100, skip: int = 0):
    query = select(Job).limit(limit).offset(skip)
    res = await db.execute(query)

    return res.scalars().all()


async def get_job_by_id(db: AsyncSession, job_id: int):
    query = select(Job).where(Job.id == job_id).limit(1)
    res = await db.execute(query)

    return res.scalars().first()
