from datetime import datetime

import fastapi
from dataclass_factory import Factory
from pydantic import EmailStr

from api.schemas.response_schema import SResponseForJob
from applications.command import CommandResult
from domain.do_schemas import DOUser, DOResponse
from infrastructure.repos import RepoUser, RepoResponse, RepoJob
from models import User, Response
from api.schemas import UserInSchema
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from core.security import hash_password


# async def get_by_id(db: AsyncSession, id: int) -> CommandResult:    # Optional[User]:
#     """uses only in tests"""
#     try:
#         repo_user = RepoUser(db)
#         res = await repo_user.get_by_id(id)
#         return CommandResult.success(result=res)
#     except Exception as e:
#         msg = "Ошибка при получении пользователя по идентификатору %s" % id
#         return CommandResult.fail(message=msg, exception=str(e))


# async def create(db: AsyncSession, user_schema: UserInSchema) -> CommandResult:
#     # uses only in tests
#     user_do = DOUser(
#         name=user_schema.name,
#         email=user_schema.email,
#         hashed_password=hash_password(user_schema.password),
#         is_company=user_schema.is_company,
#         created_at=datetime.utcnow(),
#     )
#     repo_user = RepoUser(db)
#     try:
#         res = await repo_user.add(user_do)
#         return CommandResult.success(result=res)
#     except Exception as e:
#         msg = "Ошибка при добавлении объекта user"
#         return CommandResult.fail(message=msg, exception=str(e))


# async def update(db: AsyncSession, user: User) -> CommandResult:  # User:
#     """only used in test"""
#     try:
#         await db.merge(user)  # add(user) # TODO: check, debug
#         await db.commit()
#         await db.refresh(user)
#         return CommandResult.success(result=user)
#     except Exception as e:
#         msg = "Ошибка в ходе редактирования пользователя %s, %s" % (user.id, user.name)
#         return CommandResult.fail(message=msg, exception=str(e))


async def update_current_user(
        id: int,
        user: DOUser,
        db: AsyncSession,
        current_user_mail: str) -> CommandResult:
    repo_user = RepoUser(db)
    old_user = await repo_user.get_by_id(id)

    if old_user is None or old_user.email != current_user_mail:
        msg = "Пользователь не найден или пытается редактировать не свои данные"
        return CommandResult.fail(message=msg)

    old_user.name = user.name if user.name is not None else old_user.name
    old_user.email = user.email if user.email is not None else old_user.email
    old_user.is_company = user.is_company if user.is_company is not None else old_user.is_company

    result = await repo_user.update(old_user)
    return result


async def get_by_email(db: AsyncSession, email: EmailStr) -> DOUser:
    try:
        repo_user = RepoUser(db)
        res = await repo_user.get_by_email(email)
        return res
    except:
        return None

# async def response_job(
#     db: AsyncSession,
#     job_id: int,
#     ):
#     """Записывает в базу отклик на указанную вакансию
#
#     По ТЗ требовалась реализация метода с такой сигнатурой.
#     Но странно фиксировать отклики, не указывая, кто откликнулся"""
#     repo_resp = RepoResponse(db)
#     apply_for_vacancy = DOResponse(
#         user_id=None,
#         job_id=job_id,
#         message=None,
#     )
#     repo_resp.add(apply_for_vacancy)

async def respond_to_vacancy(
    db: AsyncSession,
    vacancy_response_schema: SResponseForJob,
    ) -> Response:
    """Записывает в базу отклик на указанную вакансию"""
    try:
        repo_resp = RepoResponse(db)
        repo_job = RepoJob(db)
        job = await repo_job.get_by_id(vacancy_response_schema.job_id)
        if not job:
            msg = "Вакансия с идентификатором %s не найдена в базе" % vacancy_response_schema.job_id
            # return CommandResult.fail(message=msg)
            raise fastapi.HTTPException(
                status_code=fastapi.status.HTTP_400_BAD_REQUEST,
                detail=msg,
            )

        apply_for_vacancy = DOResponse(
            user_id=vacancy_response_schema.user_id,
            job_id=vacancy_response_schema.job_id,
            message=vacancy_response_schema.message,
        )
        new_resp = await repo_resp.add(apply_for_vacancy)
        return new_resp

    except Exception as e:
        msg = "Ошибка при создании отклика на вакансию"
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_400_BAD_REQUEST,
            detail=msg,
        )