from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import Response
from schemas import ResponseCreateSchema


async def response_job(
    db: AsyncSession,
    job_id: int,
    response_schema: ResponseCreateSchema,
    user_id: int
) -> Response:
    response = Response(
        user_id=user_id,
        job_id=job_id,
        message=response_schema.message
    )
    db.add(response)
    await db.commit()
    await db.refresh(response)
    return response


async def get_responses_by_job_id(db: AsyncSession, job_id: int) -> List[Response]:
    query = select(Response).where(Response.job_id == job_id)
    res = await db.execute(query)
    return res.scalars().all()
