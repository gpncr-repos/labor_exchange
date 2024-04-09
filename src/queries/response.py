from models import Job, Response
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select


async def get_response_by_job_id(db: AsyncSession, job_id: int) -> Optional[Response]:
    query = select(Response).where(Job.id == job_id)
    res = await db.execute(query)
    return res.scalars().first()
