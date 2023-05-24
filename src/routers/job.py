from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import get_db, get_current_user
from dependencies.job import get_current_job
from models import User, Job
from queries import job as job_queries
from queries.job import get_response_by_job_id
from schemas.job import CreateJobRequest, CreateJobResponse, GetJobResponse, CreateResponseRequest, \
    GetResponseUserResponse, GetResponseResponse

router = APIRouter(prefix="/jobs", tags=["jobs"])


@router.post("", response_model=CreateJobResponse)
async def create_job(job: CreateJobRequest,
                     db: AsyncSession = Depends(get_db),
                     current_user: User = Depends(get_current_user)):
    if not current_user.is_company:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Пользователь не может создать вакансию")

    created_job = await job_queries.create_job(db=db, user_id=current_user.id, job_schema=job)
    return CreateJobResponse.from_orm(created_job)


@router.get("/{job_id}", response_model=GetJobResponse)
async def get_job(job: Job = Depends(get_current_job), db: AsyncSession = Depends(get_db)):
    job = await job_queries.get_job_by_id(db=db, id=job.id)
    if job is None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="Данная вакансия отсутствует")
    return GetJobResponse.from_orm(job)


@router.delete("/{job_id}")
async def remove_job(job: Job = Depends(get_current_job),
                     db: AsyncSession = Depends(get_db),
                     current_user: User = Depends(get_current_user),
                     ):
    if not current_user.is_company:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="Пользователь не может удалять вакансию")

    await job_queries.remove_job(db=db, id=job.id)


@router.put("/{job_id}", response_model=CreateJobResponse)
async def update_job(job_request: CreateJobRequest,
                     job: Job = Depends(get_current_job),
                     db: AsyncSession = Depends(get_db),
                     current_user: User = Depends(get_current_user),
                     ):
    if not current_user.is_company:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="Пользователь не может редактировать вакансию")

    old_job = job
    old_job.title = job_request.title if job_request.title is not None else old_job.title
    old_job.description = job_request.description if job_request.description is not None else old_job.description
    old_job.salary_from = job_request.salary_from if job_request.salary_from is not None else old_job.salary_from
    old_job.salary_to = job_request.salary_to if job_request.salary_to is not None else old_job.salary_to
    old_job.is_active = job_request.is_active if job_request.is_active is not None else old_job.is_active
    new_job = await job_queries.update_job(db=db, job_model=old_job)

    return CreateJobResponse.from_orm(new_job)


@router.get("", response_model=List[GetJobResponse])
async def get_all_jobs(db: AsyncSession = Depends(get_db)):
    jobs = await job_queries.get_all_jobs(db=db)
    return jobs


@router.post("/{job_id}/response")
async def create_response(response_schema: CreateResponseRequest,
                          job: Job = Depends(get_current_job),
                          db: AsyncSession = Depends(get_db),
                          current_user: User = Depends(get_current_user),
                          ):
    if current_user.is_company:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Компания не может откликаться на вакансию")

    await job_queries.create_response(db, job.id, current_user.id, response_schema)


@router.get("/{job_id}/response", response_model=List[GetResponseResponse])
async def get_response_by_job(job: Job = Depends(get_current_job),
                              db: AsyncSession = Depends(get_db),
                              current_user: User = Depends(get_current_user),
                              ):
    if not current_user.is_company:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="Пользователь не может смотреть отклики на вакансию")

    result = await get_response_by_job_id(db, job.id)
    return [GetResponseResponse(message=i.message, user=GetResponseUserResponse(email=i.user.email, name=i.user.name))
            for i in result]
