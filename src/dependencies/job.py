from fastapi import Depends, HTTPException, status
from queries import job as job_queries
from sqlalchemy.ext.asyncio import AsyncSession
from dependencies.db import get_db
from models import Job


async def get_current_job(job_id:int, db: AsyncSession = Depends(get_db)) -> Job:
    cred_exception = HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Данная вакансия отсутствует")
    job = await job_queries.get_job_by_id(db=db, id=job_id)
    if job is None:
        raise cred_exception
    return job
