import logging

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

import src.queries.job as job_queries
from src.database.tables import User
from src.dependencies import get_current_user, get_session
from src.schemas.job import JobSchema
from utils import check_is_company, check_is_owner

router = APIRouter(prefix="/jobs", tags=["jobs"])


@router.post("/create_job", response_class=Response)
async def create_job(
    job_schema: JobSchema, session: AsyncSession = Depends(get_session), current_user: User = Depends(get_current_user)
):
    logging.info(f"the job creation request was received from user id {job_schema.user_id}")
    check_is_company(current_user.is_company, "Вы не можете обновлять вакансии, т.к. являетесь физическим лицом.")

    await job_queries.create_new_job(job_schema, session)
    logging.info(f"the vacancy has been created, the owner is the user id {job_schema.user_id}")
    return Response(status_code=status.HTTP_201_CREATED)


@router.get("/get_jobs", response_model=list[JobSchema])
async def get_jobs(
    limit: int = 100,
    skip: int = 0,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    logging.info(f"request was received to receive {limit} users, offset {skip}")
    results = await job_queries.get_all_jobs(session=session, limit=limit, skip=skip)
    logging.info(f"{len(results)} users have been successfully received")
    return results


@router.get("/get_job/{id}", response_model=JobSchema)
async def get_job(
    id: int, session: AsyncSession = Depends(get_session), current_user: User = Depends(get_current_user)
):
    logging.info(f"data on the {id} id job has been requested")
    job = await job_queries.get_job_by_id(id=id, session=session)
    if not job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Вакансия не найдена.")
    logging.info(f"the data on the job {id} id has been received")
    return job


@router.put("/update_job/{job_id}", response_class=Response)
async def update_job(
    job_id: int,
    job: JobSchema,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    logging.info(f"a request was received to update job id {job_id} data")
    check_is_company(current_user.is_company, "Вы не можете обновлять вакансии, т.к. являетесь физическим лицом.")
    check_is_owner(job_id, current_user.id, "Вы не можете обновлять вакансию, которая не является Вашей.")

    old_job = await job_queries.get_job_by_id(id=job_id, session=session, lock=True)

    if old_job is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Вакансия не найдена.")
    await job_queries.update_job_by_id(session=session, old_job=old_job, new_job=job)

    logging.info(f"the data of the job id {id} has been updated")

    return Response(status_code=status.HTTP_204_NO_CONTENT)
