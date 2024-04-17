from typing import List

from sqlalchemy import select
from sqlalchemy.exc import NoResultFound, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from models import Job
from schemas import JobInSchema


async def create_job(db: AsyncSession, job_schema: JobInSchema, user_id: int) -> Job:
    try:
        job = Job(
            user_id=user_id,
            title=job_schema.title,
            description=job_schema.description,
            salary_from=job_schema.salary_from,
            salary_to=job_schema.salary_to,
        )
        db.add(job)
        await db.commit()
        await db.refresh(job)
        return job
    except SQLAlchemyError as e:
        await db.rollback()
        raise ValueError("При создании вакансии произошла ошибка.") from e


async def get_all_jobs(db: AsyncSession, limit: int = 100, skip: int = 0) -> List[Job]:
    query = select(Job).limit(limit).offset(skip)
    res = await db.execute(query)
    return res.scalars().all()


async def get_job_by_id(db: AsyncSession, job_id: int) -> Job:
    query = select(Job).where(Job.id == job_id).limit(1)
    res = await db.execute(query)
    return res.scalars().first()


async def delete_job(db: AsyncSession, job_id: int) -> Job:
    try:
        query = select(Job).where(Job.id == job_id)
        res = await db.execute(query)
        job = res.scalar_one()

        await db.delete(job)
        await db.commit()
        return job
    except NoResultFound:
        await db.rollback()
        raise ValueError("Вакансия не найдена")
    except Exception as e:
        await db.rollback()
        raise e


async def update_job(db: AsyncSession, job_id: int, update_data: dict) -> Job:
    try:
        stmt = select(Job).where(Job.id == job_id)
        result = await db.execute(stmt)
        job = result.scalar_one()

        for key, value in update_data.items():
            setattr(job, key, value)

        await db.commit()
        await db.refresh(job)
        return job
    except NoResultFound:
        await db.rollback()
        raise ValueError("Вакансия не найдена")
    except Exception as e:
        await db.rollback()
        raise e
