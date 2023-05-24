from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from schemas import JobSchema, JobInSchema, JobCreateSchema
from dependencies import get_db, get_current_user
from sqlalchemy.ext.asyncio import AsyncSession
from queries import job as job_queries
from models import Job, User


router = APIRouter(prefix="/jobs", tags=["jobs"])


@router.get("", response_model=List[JobSchema])
async def get_all_jobs(
    db: AsyncSession = Depends(get_db), limit: int = 100, skip: int = 0
):
    return await job_queries.get_all(db=db, limit=limit, skip=skip)


@router.get("", response_model=List[JobSchema])
async def get_job_by_id(job_id: int, db: AsyncSession = Depends(get_db)):
    return await job_queries.get_by_id(db=db, job_id=job_id)


@router.post("", response_model=JobSchema)
async def create_job(
    job_schema: JobInSchema,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if not current_user.is_company:
        raise HTTPException(
            status_code=403, detail="Вакансию могут создавать только работодатели"
        )
    job_create_schema = JobCreateSchema(
        user_id=current_user.id,
        title=job_schema.title,
        description=job_schema.description,
        salary_from=job_schema.salary_from,
        salary_to=job_schema.salary_to,
        is_active=job_schema.is_active,
    )
    job = await job_queries.create(db=db, job_schema=job_create_schema)
    return JobSchema.from_orm(job)
