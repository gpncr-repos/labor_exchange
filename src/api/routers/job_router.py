from typing import List

from fastapi import APIRouter, Depends, HTTPException, status, Body
from sqlalchemy.ext.asyncio import AsyncSession

from api.schemas.job_schemas import SJob, SRemoveJobReport
from applications.dependencies import get_current_user, get_db
from applications.dependencies.db import get_repo_job
from applications.dependencies.user import get_current_employer
from domain.dm_schemas import DMJob
from infrastructure.repos import RepoJob
from models import User

router = APIRouter(
    prefix="/job",
    tags=["vacancies"],
)

@router.post("",
             summary="Разместить вакансию",
             response_model=SJob)
async def place_job(
        job_in_schema: SJob = Body(description="Характеристики вакансии"),
        current_employer: User = Depends(get_current_employer),
        repo_job: RepoJob= Depends(get_repo_job),
    ):
    """
    Добавляет в таблицу jobs запись-вакансию  с переданными параметрами по запросу пользователя-работодателя

    :param job_in_schema: SJob объект параметры вакансии
    :param current_employer: User объект пользователь автор вакансии
    :param repo_job: RepoJob репозиторий для работы с базой данных
    :returns: пары поле:значение добавленной записи
    :rtype: SJob
    """
    job_dm = DMJob(
        user_id=current_employer.id,
        title=job_in_schema.title,
        description=job_in_schema.description,
        salary_from=job_in_schema.salary_from,
        salary_to=job_in_schema.salary_to,
        is_active=job_in_schema.is_active,
        created_at=job_in_schema.utcnow()
    )
    res = await repo_job.add(job_dm)
    return SJob.from_orm(res)

@router.get("/jobs",
            summary="Получние списка вакансий",
            response_model=List[SJob],
            )
async def read_vacancies(
        repo_job: RepoJob= Depends(get_repo_job),
    ):
    """
    Возвращает список вакансий из таблицы jobs

    :param repo_job: RepoJob репозиторий для работы с базой данных
    :returs: список записей с их полями и значениями полей
    :rtype: List[SJob]
    """
    orm_objs = await repo_job.get_all()
    result = [SJob.from_orm(orm_obj) for orm_obj in orm_objs]
    return result


@router.put("/{job_id}",
            summary="Редактирование вакансии",
            response_model=SJob,
            )
async def edit_job(
        job_id: int,
        job_in_schema: SJob,
        repo_job: RepoJob= Depends(get_repo_job),
        current_user: User = Depends(get_current_user),
    ):
    """
    Заменяет параметры вакансии на переданные по запросу пользователя автора вакансии

    :param job_id: int идентификатор вакансии
    :param job_in_schema: SJob объект с новыми параметрами
    :param repo_job: RepoJob репозиторий для работы с базой данных
    :param current_user: User объект пользователь
    :returns: пары поле:значение добавленной записи
    :rtype: SJob
    """
    job_to_edit = await repo_job.get_by_id(job_id)
    if job_to_edit.user_id == current_user.id:
        job_schema = DMJob(
            id=job_id,
            title=job_in_schema.title,
            description=job_in_schema.description,
            salary_from=job_in_schema.salary_from,
            salary_to=job_in_schema.salary_to,
            is_active=job_in_schema.is_active,
        )
        updated_job = await repo_job.update(job_schema)
        # updated_job = await update_job(job_id, db, job_schema, current_user.id)
        return SJob.from_orm(updated_job)
    else:
        msg = "Пользователь %s не является автором вакансии %s, поэтому не может ее редактировать" % (current_user.name, job_id)
        raise HTTPException(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
            detail=msg,
        )

@router.delete(
    "/{job_id}",
    summary="Удаление вакансии",
    description="Удаляет вакансию по идентификатору",
    response_model=SRemoveJobReport,
)
async def delete_job(
        job_id: int,
        repo_job: RepoJob= Depends(get_repo_job),
        current_employer: User = Depends(get_current_employer),
    ):
    """
    Удаляет вакансию по запросу автора

    :param job_id: int идентификатор вакансии
    :param repo_job: RepoJob репозиторий для работы с базой данных
    :param current_employer: User объект пользователь
    :returns: сообщение об удалении вакансии
    :rtype: SRemoveJobReport
    """
    job_to_del = await repo_job.get_by_id(job_id)
    if job_to_del.user_id == current_employer.id:
        result = await repo_job.del_by_id(job_id)
        return SRemoveJobReport(id=job_id, message="Вакансия %s удалена" % result)
    else:
        msg = "Вакансия %s не была удалена; удаляющий пользователь %s не является ее автором" % (job_id, current_employer.name)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=msg
        )
