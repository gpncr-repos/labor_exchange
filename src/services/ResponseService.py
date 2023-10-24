import queries.response
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import get_current_user
from models import Job, Response, User
from queries.job import get_job_by_id
from Errors import UserPermissionError, InteractionWithInactiveObject


async def response_job(db: AsyncSession, job_id: int, current_user: User = Depends(get_current_user)):
    job = await get_job_by_id(db, job_id)

    if current_user.is_company:
        raise UserPermissionError("Company can't response")

    if not job.is_active:
        raise InteractionWithInactiveObject("job is inactive")

    await queries.response.create(db, job_id, current_user.id, "")
