from fastapi import HTTPException
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from models import Response, User
from schemas import ResponseInSchema


async def create_response(db: AsyncSession, response_scheme: ResponseInSchema, current_user: User):
    response = Response(
        user_id=current_user.id,
        job_id=response_scheme.job_id,
        message=response_scheme.message,
    )
    db.add(response)
    await db.commit()
    await db.refresh(response)
    return response


async def get_responses_by_job_id(db: AsyncSession, job_id: int):
    query = select(Response).where(Response.job_id == job_id)
    res = await db.execute(query)

    return res.scalars().all()


async def get_responses_by_user_id(db: AsyncSession, user_id: int):
    query = select(Response).where(Response.user_id == user_id)
    res = await db.execute(query)
    return res.scalars().all()


async def delete_response_by_id(db: AsyncSession, response_id, current_user: User):
    response = await db.get(Response, response_id)

    if response is None:
        raise HTTPException(status_code=404, detail="Такого отклика нет")
    if response.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Вы не владелец этого отклика")

    delete_response = delete(Response).where(Response.id == response_id)
    await db.execute(delete_response)
    await db.commit()
    return True
