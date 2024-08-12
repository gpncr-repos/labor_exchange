"""" Model Jobs API  """

import json
from typing import List

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import get_current_user, get_db
from models import User
from queries import jobs as jobs_queries
from schemas import JobCreateSchema, JobSchema, JobUpdateSchema

from .response_examples.jobs import (
    responses_delete_jobs,
    responses_get_jobs,
    responses_post_jobs,
    responses_update_jobs,
)
from .validation import Real_Validation

router = APIRouter(prefix="/jobs", tags=["jobs"])


@router.get("/{job_id}", response_model=JobSchema, responses={**responses_get_jobs})
async def get_job_by_id(job_id: int, db: AsyncSession = Depends(get_db)):
    """
    Get job by id:\n
    job_id: job id\n
    db: datebase connection;\n
    """
    job_by_id = await jobs_queries.get_by_id(db=db, job_id=job_id)
    Real_Validation.element_not_found(job_by_id)
    return JobSchema(**job_by_id.__dict__)


@router.get("", response_model=List[JobSchema], responses={**responses_get_jobs})
async def get_all_jobs(db: AsyncSession = Depends(get_db), limit: int = 100, skip: int = 0):
    """
    Get limit Jobs skip some:\n
    db: datebase connection;\n
    limit: limits of Jobs,\n
    skip: skip from:
    """
    all_jobs = await jobs_queries.get_all(db=db, limit=limit, skip=skip)
    Real_Validation.element_not_found(all_jobs)
    list_of_jobs = []
    for job in all_jobs:
        list_of_jobs.append(JobSchema(**job.__dict__))
    return list_of_jobs


@router.post("", response_model=JobSchema, responses={**responses_post_jobs})
async def create_job(
    job: JobCreateSchema,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Create job:\n
    job: dataset of JobCreateSchema\n
    db: datebase connection;\n
    """
    Real_Validation.is_company_for_job(current_user.is_company)
    created_job = await jobs_queries.create(db=db, job_schema=job, curent_user_id=current_user.id)
    return JSONResponse(
        status_code=201, content=json.dumps(JobSchema(**created_job.__dict__).__dict__, default=str)
    )


@router.patch("", response_model=JobSchema, responses={**responses_update_jobs})
async def patch_of_job(
    jobpatch: JobUpdateSchema,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Patch job:\n
    job_id: job id\n
    job: dataset of JobUpdateSchema\n
    db: datebase connection;\n
    """
    old_job = await jobs_queries.get_by_id(db=db, job_id=jobpatch.id)
    Real_Validation.element_not_found(old_job)
    Real_Validation.is_company_for_job(current_user.is_company)
    Real_Validation.element_not_current_user_for(
        current_user.id, old_job.user_id, router_name="job", action_name="update"
    )
    old_job.title = jobpatch.title if jobpatch.title is not None else old_job.title
    old_job.salary_to = jobpatch.salary_to if jobpatch.salary_to is not None else old_job.salary_to
    old_job.salary_from = (
        jobpatch.salary_from if jobpatch.salary_from is not None else old_job.salary_from
    )
    old_job.discription = (
        jobpatch.discription if jobpatch.discription is not None else old_job.discription
    )
    old_job.is_active = jobpatch.is_active if jobpatch.is_active is not None else old_job.is_active
    update_job = await jobs_queries.update(db=db, update_job=old_job)
    return JobSchema(**update_job.__dict__)


@router.delete("/{job_id}", responses={**responses_delete_jobs})
async def delete_job(
    job_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Delete job:\n
    job_id: job id\n
    db: datebase connection;\n
    """
    job_to_delete = await jobs_queries.get_by_id(db=db, job_id=job_id)
    Real_Validation.element_not_found(job_to_delete)
    Real_Validation.is_company_for_job(current_user.is_company)
    Real_Validation.element_not_current_user_for(
        current_user.id, job_to_delete.user_id, router_name="job", action_name="delete"
    )
    removed_job = await jobs_queries.delete(db=db, delete_job=job_to_delete)
    return JobSchema(**removed_job.__dict__)
