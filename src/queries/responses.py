from models import Response, Job
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Sequence, Optional


async def get_response_by_id(db: AsyncSession, id: int) -> Optional[Response]:
    query = select(Response).where(Response.id == id).limit(1)
    res = await db.execute(query)
    return res.scalars().first()


async def get_response_by_job_id(db: AsyncSession, job_id: int) -> Sequence[Response]:
    query = select(Response).where(Response.job_id == job_id)
    res = await db.execute(query)
    return res.scalars().all()


async def delete_some_responses(db: AsyncSession, responses: Sequence[Response]) -> Sequence[Response]:
    for i in responses:
        await db.delete(i)
    await db.commit()
    return responses


async def get_response_by_user_id(db: AsyncSession, user_id: int, choice: int) -> Sequence[Response]:
    if choice == 0:
        query = select(Response).where(Response.job.user_id == user_id)
    else:
        query = select(Response).where(Response.user_id == user_id)
    res = await db.execute(query)
    return res.scalars().all()


async def update_response(db: AsyncSession, response: Response) -> Response:
    db.add(response)
    await db.commit()
    await db.refresh(response)
    return response


async def response_job(db: AsyncSession, user_id: int, job_id: int, message: str) -> Response:
    response = Response(
        user_id=user_id,
        job_id=job_id,
        message=message
    )
    db.add(response)
    await db.commit()
    await db.refresh(response)
    return response


async def delete_response(db: AsyncSession, response: Response) -> Response:
    await db.delete(response)
    await db.commit()
    return response
