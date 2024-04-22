from models import Job, Response
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from schemas.response import ResponseInSchema


async def get_response_by_job_id(db: AsyncSession, job_id: int) -> Optional[Response]:
    query = select(Response).where(Job.id == job_id)
    res = await db.execute(query)
    return res.scalars().first()


async def update_response(db: AsyncSession, response: Response) -> Response:
    db.add(response)
    await db.commit()
    await db.refresh(response)
    return response


async def create_response(db: AsyncSession, response_schema: ResponseInSchema) -> Job:
    response = Response(
        title=response_schema.message,
    )
    db.add(response)
    await db.commit()
    await db.refresh(response)
    return response
