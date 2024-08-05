"""" Model Jobs API  """

from typing import List

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import get_current_user, get_db
from models import User
from queries import jobs as jobs_queries
from schemas import JobCreateSchema, JobSchema, JobUpdateSchema

from .validation import Validation_for_routers

router = APIRouter(prefix="/jobs", tags=["jobs"])


@router.get("/{job_id}", response_model=JobSchema)
async def get_job_by_id(job_id: int, db: AsyncSession = Depends(get_db)):
    """
    Get job by id:
    job_id: job id
    db: datebase connection;
    """
    job_by_id = await jobs_queries.get_by_id(db=db, id=job_id)
    if not job_by_id:
        return Validation_for_routers.element_not_found(f"Job id {job_id}")
    return job_by_id


@router.get("", response_model=List[JobSchema])
async def get_all_jobs(
    db: AsyncSession = Depends(get_db), limit: int = 100, skip: int = 0
):
    """
    Get limit Jobs skip some:
    db: datebase connection;
    limit: limits of Jobs,
    skip: skip from:
    """
    all_jobs = await jobs_queries.get_all(db=db, limit=limit, skip=skip)
    if not all_jobs:
        return Validation_for_routers.empty_base(router_name="Job")
    return all_jobs


@router.post("/post_job", response_model=JobSchema)
async def create_job(
    job: JobCreateSchema,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Create job:
    job: dataset of JobCreateSchema
    db: datebase connection;
    """
    if not current_user.is_company:
        return JSONResponse(status_code=422, content={"message": "User is not company"})
    created_job = await jobs_queries.create(
        db=db, job_schema=job, curent_user_id=current_user.id
    )
    return JSONResponse(
        status_code=200,
        content={
            "message": "Job create",
            "Jb id": created_job.id,
            "Job Title": created_job.title,
            "Job discription": created_job.discription,
            "Job salary from": created_job.salary_from,
            "Job salary to": created_job.salary_to,
        },
    )


@router.patch("/patch_job/{job_id}", response_model=JobSchema)
async def patch_of_job(
    job_id: int,
    jobpatch: JobUpdateSchema,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Patch job:
    job_id: job id
    job: dataset of JobUpdateSchema
    db: datebase connection;
    """
    old_job = await jobs_queries.get_by_id(db=db, id=job_id)
    if current_user.id != old_job.user_id:
        return Validation_for_routers.element_not_current_user_for(
            router_name="job", action_name="update"
        )
    old_job.title = jobpatch.title if jobpatch.title is not None else old_job.title
    old_job.salary_to = (
        jobpatch.salary_to if jobpatch.salary_to is not None else old_job.salary_to
    )
    old_job.salary_from = (
        jobpatch.salary_from
        if jobpatch.salary_from is not None
        else old_job.salary_from
    )
    old_job.discription = (
        jobpatch.discription
        if jobpatch.discription is not None
        else old_job.discription
    )
    old_job.is_active = (
        jobpatch.is_active if jobpatch.is_active is not None else old_job.is_active
    )
    update_job = await jobs_queries.update(db=db, update_job=old_job)
    return JSONResponse(
        status_code=200,
        content={
            "message": "Job update",
            "Jb id": update_job.id,
            "Job Title": update_job.title,
            "Job discription": update_job.discription,
            "Job salary from": update_job.salary_from,
            "Job salary to": update_job.salary_to,
        },
    )


@router.delete("/delete/{job_id}")
async def delete_job(
    job_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Delete job:
    job_id: job id
    db: datebase connection;
    """
    job_to_delete = await jobs_queries.get_by_id(db=db, id=job_id)
    if job_to_delete is None:
        return Validation_for_routers.element_not_found(f"Job id {job_id}")
    if current_user.id != job_to_delete.user_id:
        return Validation_for_routers.element_not_current_user_for(
            router_name="job", action_name="delete"
        )
    removed_job = await jobs_queries.delete(db=db, delete_job=job_to_delete)
    return JSONResponse(
        status_code=200,
        content={
            "message": "Job update",
            "Jb id": removed_job.id,
            "Job Title": removed_job.title,
            "Job discription": removed_job.discription,
            "Job salary from": removed_job.salary_from,
            "Job salary to": removed_job.salary_to,
        },
    )
