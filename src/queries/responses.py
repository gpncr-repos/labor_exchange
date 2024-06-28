from models import Response, Job
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Sequence


async def get_all_responses(db: AsyncSession, limit: int = 100, skip: int = 0) -> Sequence[Response]:
    query = select(Response).limit(limit).offset(skip)
    res = await db.execute(query)
    return res.scalars().all()


async def get_response_by_user_id(db: AsyncSession, user_id: int) -> Sequence[Response]:
    query = select(Response).where(Response.user_id == user_id)
    res = await db.execute(query)
    return res.scalars().all()


async def get_response_by_employer_id(db: AsyncSession, user_id: int) -> Sequence[Response]:
    query = select(Response).where(Response.job_id == Job.id).where(Job.user_id == user_id)
    res = await db.execute(query)
    return res.scalars().all()


async def response_job(db: AsyncSession, user_id: int, job_id: int, message: str):
    response = Response(
        user_id=user_id,
        job_id=job_id,
        message=message
    )
    db.add(response)
    await db.commit()
    await db.refresh(response)
    return response
