"""Сценарии, работающие с базой данных"""
from decimal import Decimal

from sqlalchemy.ext.asyncio import AsyncSession

from api.schemas.job_schemas import SJob
from applications.schemas.schemas import JobDO
from infrastructure.repos import RepoJob
from models import Job


def convert_job_schema_to_do(user_id: int, job_schema: SJob) -> JobDO:
    """Преобразует данные для создания записи в DO"""
    result = JobDO(
        user_id=user_id,
        title=job_schema.title,
        description=job_schema.description,
        salary_from=job_schema.salary_from,
        salary_to=job_schema.salary_to,
        is_active=job_schema.is_active,
    )
    return result

async def create_job(db: AsyncSession, job_schema: JobDO):
    """Добавляет запись в таблицу jobs

    param: db: AsyncSession - объект сессия подключения к базе данных
    param: job_schema: SJob - объект, который требуется внести в таблицу
    """
    try:
        repo_job = RepoJob(db)
        job_to_add = Job(
            user_id=job_schema.user_id,
            title=job_schema.title,
            description=job_schema.description,
            salary_from=Decimal(job_schema.salary_from),
            salary_to=Decimal(job_schema.salary_to),
            is_active=job_schema.is_active,
        )
        db.add(job_to_add)
        await db.commit()
        await db.refresh(job_to_add)
        # result = await repo_job.add(job_to_add)
    except Exception as e:
        msg = "Ошибка при добавлении вакансии %s пользователем %s; %s" %(job_schema.title, job_schema.user_id, e)
        raise Exception()

async def get_all_jobs(self, db: AsyncSession, limit: int = 100, skip: int = 0) -> Job:
    try:
        repo_job = RepoJob(db)
        result = await repo_job.get_all(limit, skip)
        return result
    except Exception as e:
        msg = "Ошибка при получении списка вакансий; %s" % (str(e))
        raise Exception(msg)

async def get_job_by_id(self, db: AsyncSession, job_id: int):
    try:
        repo_job = RepoJob(db)
        result = await repo_job.get_by_id(job_id)
        return result
    except Exception as e:
        msg = "Ошибка при получении вакансии по идентификатору %s; %s" % (job_id, str(e))
        raise Exception(msg)
