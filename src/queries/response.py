from typing import List
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import Response


async def create(db: AsyncSession, job_id: int, user_id: int, message: str) -> Response:
    new_response = Response(
        job_id=job_id,
        user_id=user_id,
        message=message
    )
    db.add(new_response)
    await db.commit()
    await db.refresh(new_response)
    return new_response


async def get_response_by_user_id(db: AsyncSession, job_id: int) -> List[Response]:
    request = select(Response).where(Response.user_id == job_id)
    result = await db.execute(request)
    list_of_jobs = result.fetchall()
    return list_of_jobs
