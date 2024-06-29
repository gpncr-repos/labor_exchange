from models import Response, Job
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Sequence, Optional


async def get_response_by_id(db: AsyncSession, id: int) -> Optional[Response]:
    query = select(Response).where(Response.id == id).limit(1)
    res = await db.execute(query)
    return res.scalars().first()


async def get_response_by_user_id(db: AsyncSession, user_id: int) -> Sequence[Response]:
    query = select(Response).where(Response.user_id == user_id)
    res = await db.execute(query)
    return res.scalars().all()


async def get_response_by_employer_id(db: AsyncSession, user_id: int) -> Sequence[Response]:
    query = select(Response).where(Response.job_id == Job.id).where(Job.user_id == user_id).where(Job.is_active == True)
    res = await db.execute(query)
    return res.scalars().all()


async def update(db: AsyncSession, response: Response) -> Response:
    db.add(response)
    await db.commit()
    await db.refresh(response)
    return response


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
