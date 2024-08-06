"""" Model Jobs API  """

from typing import List

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import get_current_user, get_db
from models import User
from queries import jobs as jobs_queries
from schemas import JobCreateSchema, JobSchema, JobUpdateSchema

from .validation import Real_Validation

router = APIRouter(prefix="/jobs", tags=["jobs"])
responses = {
    204: {"description": "Zero rezult"},
    403: {"description": "You have not power here"},
    422: {"description": "Some proplem with validation"},
}
responses_get = {
    **responses,
    200: {
        "description": "Get job",
        "content": {
            "application/json": {
                "example": {
                    "message": "Job get",
                    "Job id": 1,
                    "Job Title": "President",
                    "Job discription": "Sir",
                    "Job salary from": 100000,
                    "Job salary to": 200000,
                    "Job active": True,
                    "Job created_at": "2024-08-06T20:41:48.521Z",
                }
            }
        },
    },
}

responses_post = {
    **responses,
    200: {
        "description": "job create",
        "content": {
            "application/json": {
                "example": {
                    "message": "Job create",
                    "Job id": 1,
                    "Job Title": "President",
                    "Job discription": "Sir",
                    "Job salary from": 100000,
                    "Job salary to": 200000,
                    "Job created_at": "2024-08-06T20:41:48.521Z",
                }
            }
        },
    },
}

responses_update = {
    **responses,
    200: {
        "description": "job updated",
        "content": {
            "application/json": {
                "example": {
                    "message": "Job update",
                    "Job id": 1,
                    "Job Title": "President",
                    "Job discription": "Sir",
                    "Job salary from": 100000,
                    "Job salary to": 200000,
                }
            }
        },
    },
}
responses_delete = {
    **responses,
    200: {
        "description": "job delete",
        "content": {
            "application/json": {
                "example": {
                    "message": "Job delete",
                    "Job id": 1,
                    "Job Title": "President",
                    "Job discription": "Sir",
                    "Job salary from": 100000,
                    "Job salary to": 200000,
                }
            }
        },
    },
}


@router.get("/{job_id}", response_model=JobSchema, responses={**responses_get})
async def get_job_by_id(job_id: int, db: AsyncSession = Depends(get_db)):
    """
    Get job by id:
    job_id: job id
    db: datebase connection;
    """
    job_by_id = await jobs_queries.get_by_id(db=db, job_id=job_id)
    Real_Validation.element_not_found(job_by_id, f"Job id {job_id}")
    return job_by_id


@router.get("", response_model=List[JobSchema], responses={**responses_get})
async def get_all_jobs(db: AsyncSession = Depends(get_db), limit: int = 100, skip: int = 0):
    """
    Get limit Jobs skip some:
    db: datebase connection;
    limit: limits of Jobs,
    skip: skip from:
    """
    all_jobs = await jobs_queries.get_all(db=db, limit=limit, skip=skip)
    Real_Validation.empty_base(all_jobs, router_name="Job")
    return all_jobs


@router.post("/post_job", response_model=JobSchema, responses={**responses_post})
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
    Real_Validation.is_company_for_job(current_user.is_company)
    created_job = await jobs_queries.create(db=db, job_schema=job, curent_user_id=current_user.id)
    return JSONResponse(
        status_code=200,
        content={
            "message": "Job create",
            "Job id": created_job.id,
            "Job Title": created_job.title,
            "Job discription": created_job.discription,
            "Job salary from": created_job.salary_from,
            "Job salary to": created_job.salary_to,
            "Job created at": str(created_job.created_at),
        },
    )


@router.patch("/patch_job/{job_id}", response_model=JobSchema, responses={**responses_update})
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
    old_job = await jobs_queries.get_by_id(db=db, job_id=job_id)
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
    return JSONResponse(
        status_code=200,
        content={
            "message": "Job update",
            "Job id": update_job.id,
            "Job Title": update_job.title,
            "Job discription": update_job.discription,
            "Job salary from": update_job.salary_from,
            "Job salary to": update_job.salary_to,
        },
    )


@router.delete("/delete/{job_id}", responses={**responses_delete})
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
    job_to_delete = await jobs_queries.get_by_id(db=db, job_id=job_id)
    Real_Validation.element_not_found(job_to_delete, f"Job id {job_id}")
    Real_Validation.element_not_current_user_for(
        current_user.id, job_to_delete.user_id, router_name="job", action_name="delete"
    )
    removed_job = await jobs_queries.delete(db=db, delete_job=job_to_delete)
    return JSONResponse(
        status_code=200,
        content={
            "message": "Job delete",
            "Job id": removed_job.id,
            "Job Title": removed_job.title,
            "Job discription": removed_job.discription,
            "Job salary from": removed_job.salary_from,
            "Job salary to": removed_job.salary_to,
        },
    )
