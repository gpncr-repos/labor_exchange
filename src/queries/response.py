from models import Response
from schemas import ResponseCreateSchema
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select


async def get_by_job_id(db: AsyncSession, job_id: int) -> List[Response]:
    query = select(Response).where(Response.job_id == job_id)
    res = await db.execute(query)
    return res.scalars().all()


async def create(db: AsyncSession, response_schema: ResponseCreateSchema) -> Response:
    response = Response(
        user_id=response_schema.user_id,
        job_id=response_schema.job_id,
        message=response_schema.message,
    )
    db.add(response)
    await db.commit()
    await db.refresh(response)
    return response
