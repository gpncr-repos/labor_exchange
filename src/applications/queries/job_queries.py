"""Сценарии, работающие с базой данных"""
from datetime import datetime
from decimal import Decimal

import fastapi
from fastapi import status
from sqlalchemy.ext.asyncio import AsyncSession

from api.schemas.job_schemas import SJob
from domain.do_schemas import DOJob, DOJobEdit
from infrastructure.repos import RepoJob
from models import Job


def convert_job_schema_to_do(user_id: int, job_schema: SJob) -> DOJob:
    """Преобразует данные для создания записи в DO"""
    result = DOJob(
        user_id=user_id,
        title=job_schema.title,
        description=job_schema.description,
        salary_from=job_schema.salary_from,
        salary_to=job_schema.salary_to,
        is_active=job_schema.is_active,
        created_at=datetime.utcnow()
    )
    return result


async def create_job(db: AsyncSession, job_schema: DOJob) -> Job:
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
        res = await repo_job.add(job_to_add)
        return res
    except Exception as e:
        msg = "Ошибка при добавлении вакансии %s пользователем %s; %s" % (job_schema.title, job_schema.user_id, e)
        raise fastapi.HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=msg,
        )


async def update_job(
        job_id: int,
        db: AsyncSession,
        job_schema: DOJobEdit,
        current_user_id: int,
):
    repo_job = RepoJob(db)
    job_to_edit = await repo_job.get_by_id(job_id)
    if job_to_edit.user_id == current_user_id:
        job_to_edit.title = job_schema.title
        job_to_edit.description = job_schema.description
        job_to_edit.salary_from = job_schema.salary_from
        job_to_edit.salary_to = job_schema.salary_to
        job_to_edit.is_active = job_schema.is_active

        updated_job = await repo_job.update(job_to_edit)
        return updated_job


async def delete_job_by_id(db: AsyncSession, job_id: int, author_id: int):
    repo_job = RepoJob(db)
    job_to_del = await repo_job.get_by_id(job_id)
    if job_to_del and job_to_del.user_id == author_id:
        result = await repo_job.del_by_id(job_id)
        if result == job_id:
            return
    else:
        raise fastapi.HTTPException(
            detail="Вакансия %s не была удалена; либо она не найдена, либо удаляющий пользователь не является ее автором" % job_id,
            status_code=status.HTTP_400_BAD_REQUEST,
        )
