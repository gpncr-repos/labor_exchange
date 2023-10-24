from typing import List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import Response
from schemas import ResponseSchema


async def create(db: AsyncSession, response: ResponseSchema) -> Response:
    new_response = Response(
        job_id=response.job_id,
        user_id=response.user_id,
        message=response.message
    )
    db.add(new_response)
    await db.commit()
    await db.refresh(new_response)
    return new_response


async def get_response_by_user_id(db: AsyncSession, job_id: str) -> List[Response]:
    request = select(Response).where(Response.user_id == int(job_id))
    result = await db.execute(request)
    list_of_jobs = result.fetchall()
    return list_of_jobs
