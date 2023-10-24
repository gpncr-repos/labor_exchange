import queries.response
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import get_current_user
from models import Job, Response, User
from queries.job import get_job_by_id
from services.errors import UserPermissionError, InteractionWithInactiveObject
from schemas import ResponseSchema


async def response_job(db: AsyncSession, job_id: int, current_user: User):
    job = await get_job_by_id(db, job_id)

    if current_user.is_company:
        raise UserPermissionError("Company can't response")
    if not job.is_active:
        raise InteractionWithInactiveObject("job is inactive")

    await queries.response.create(db, ResponseSchema(job_id=job.id, user_id=current_user.id, message=""))
