from __future__ import annotations

from typing import List
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from queries.job import get_job_by_id

from models import Response, User
from schemas import ResponseInSchema

from fastapi import HTTPException, status


async def create_response(db: AsyncSession, response_schema: ResponseInSchema,
                          current_user: User) -> Response | HTTPException:
    job = await get_job_by_id(db=db, job_id=response_schema.job_id)

    if (job is None) or (not job.is_active):
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Такой вакансии нет или она не активна")
    elif current_user.is_company:
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail="Компании не могут оставлять отклик")

    existing_response = await get_response_by_user_and_job_id(db=db, user_id=current_user.id,
                                                              job_id=response_schema.job_id)
    if existing_response is not None:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Отклик на эту вакансию уже оставлен")

    response = Response(
        user_id=current_user.id,
        job_id=response_schema.job_id,
        message=response_schema.message,
    )

    db.add(response)
    await db.commit()
    await db.refresh(response)
    return response


async def get_response_by_user_and_job_id(db: AsyncSession, user_id: int, job_id: int) -> Response:
    query = select(Response).where(Response.user_id == user_id, Response.job_id == job_id)
    result = await db.execute(query)
    response = result.scalar()

    return response


async def get_all_responses(db: AsyncSession) -> List[Response]:
    query = select(Response)
    res = await db.execute(query)
    return res.scalars().all()


async def get_responses_by_job_id(db: AsyncSession, job_id: int) -> List[Response]:
    query = select(Response).where(Response.job_id == job_id)
    res = await db.execute(query)

    return res.scalars().all()


async def get_responses_by_user_id(db: AsyncSession, user_id: int) -> List[Response]:
    query = select(Response).where(Response.user_id == user_id)
    res = await db.execute(query)
    return res.scalars().all()


async def delete_response_by_id(db: AsyncSession, response_id, current_user: User) -> True | HTTPException:
    response = await db.get(Response, response_id)

    if response is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Такого отклика нет")
    if response.user_id != current_user.id:
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail="Вы не владелец этого отклика")

    delete_response = delete(Response).where(Response.id == response_id)
    await db.execute(delete_response)
    await db.commit()
    return True
