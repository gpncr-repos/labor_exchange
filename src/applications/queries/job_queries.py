"""Сценарии, работающие с базой данных"""
from decimal import Decimal

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from api.schemas.job_schemas import SJob
from applications.command import CommandResult
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
        await repo_job.add(job_to_add)
        return CommandResult.success(result=job_to_add.id)
    except Exception as e:
        msg = "Ошибка при добавлении вакансии %s пользователем %s; %s" %(job_schema.title, job_schema.user_id, e)
        return CommandResult.fail(message=msg)

async def get_all_jobs(db: AsyncSession, limit: int = 100, skip: int = 0) -> Job:
    try:
        repo_job = RepoJob(db)
        result = await repo_job.get_all(limit, skip)
        return CommandResult.success(result=result)
    except Exception as e:
        msg = "Ошибка при получении списка вакансий; %s" % (str(e))
        return CommandResult.fail(message=msg,exception=str(e))

async def get_job_by_id(db: AsyncSession, job_id: int):
    try:
        repo_job = RepoJob(db)
        result = await repo_job.get_by_id(job_id)
        return CommandResult.success(result=result)
    except Exception as e:
        msg = "Ошибка при получении вакансии по идентификатору %s; %s" % (job_id, str(e))
        return CommandResult.fail(message=msg,exception=str(e))

async def delete_job_by_id(db: AsyncSession, job_id: int, author_id: int):
    try:
        # query = select(Job).filter(Job.id==job_id, Job.user_id==author_id).limit(1)
        # res = await db.execute(query)
        # job_to_del = res.scalar()
        #     # del_stmt = delete(Job).filter(Job.id==job_id, Job.user_id==author_id)
        #     # await db.execute(del_stmt)
        #     # db.delete(res) "Chunked result is not mapped"
        #     await db.delete(job_to_del)
        #     await db.commit()
        #     return CommandResult.success(result="Вакансия %s удалена" % job_id)
        # else:
        #     return CommandResult.fail(errors="Вакансия %s не найдена или пользователь %s не является ее автором" % (job_id, author_id))
        repo_job = RepoJob(db)
        job_to_del = await repo_job.get_by_id(job_id)
        if job_to_del and job_to_del.user_id == author_id:
            result = await repo_job.del_by_id(job_id)
            if result == job_id:
                return CommandResult.success(result="Вакансия %s удалена" % job_id)

            else:
                return CommandResult.fail(result="Вакансия %s не была удалена" % job_id)
        else:
            return CommandResult.fail(
                errors="Вакансия %s не найдена или пользователь %s не является ее автором" % (job_id, author_id))
    except Exception as e:
        msg = "Ошибка при удалении вакансии по идентификатору %s; %s" % (job_id, str(e))
        return CommandResult.fail(message=msg, exception=str(e))
