from models import Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Sequence


async def get_all_responses(db: AsyncSession, limit: int = 100, skip: int = 0) -> Sequence[Response]:
    query = select(Response).limit(limit).offset(skip)
    res = await db.execute(query)
    return res.scalars().all()


async def get_response_by_user_id(db: AsyncSession, user_id: int) -> Sequence[Response]:
    query = select(Response).where(Response.id == user_id)
    res = await db.execute(query)
    return res.scalars().all()


async def get_response_by_job_id(db: AsyncSession, job_id: int) -> Sequence[Response]:
    query = select(Response).where(Response.id == job_id)
    res = await db.execute(query)
    return res.scalars().all()


async def response_job(db: AsyncSession, job_id: int, user_id: int):
    pass
    """    response = Response(
        job_id=job_id,
    )
    db.add(response)
    await db.commit()
    await db.refresh(response)
    return response """