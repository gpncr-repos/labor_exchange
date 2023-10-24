from datetime import datetime

from sqlalchemy_mock import AsyncSession

from models import User, Job
from schemas import JobInputSchema, JobSchema
from services.errors import UserPermissionError
import queries.job as job_query


async def create_job_by_user(db: AsyncSession, job: JobInputSchema, current_user: User) -> Job:
    if not current_user.is_company:
        raise UserPermissionError("only company able to create job")

    new_job = JobSchema(**job.dict(), user_id=current_user.id, created_at=datetime.utcnow())

    return await job_query.create_job(db=db, job_schema=new_job)
