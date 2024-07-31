from fastapi import APIRouter, Depends, HTTPException, status
from punq import Container

from api.v1.jobs.schemas import JobCreateSchema, JobSchema
from di import get_container
from core.exceptions import ApplicationException
from api.dependencies import get_current_user
from domain.entities.users import UserEntity
from logic.services.jobs.base import BaseJobService


router = APIRouter(prefix="/jobs", tags=["jobs"])


@router.get("", response_model=list[JobSchema])
async def get_all_jobs(
        container: Container = Depends(get_container),
        limit: int = 100,
        offset: int = 0
) -> list[JobSchema]:
    service: BaseJobService = container.resolve(BaseJobService)
    jobs = await service.get_job_list(limit=limit, offset=offset)
    return [JobSchema.from_entity(job) for job in jobs]


@router.post("", response_model=JobSchema)
async def create_job(
        job_in: JobCreateSchema,
        auth_user: UserEntity = Depends(get_current_user),
        container: Container = Depends(get_container),
) -> JobSchema:
    service: BaseJobService = container.resolve(BaseJobService)
    job_in.user_id = auth_user.id
    try:
        job = await service.create_job(job_in=job_in.to_entity(), auth_user=auth_user)
    except ApplicationException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e.message,
        )
    return JobSchema.from_entity(job)


@router.put("", response_model=JobSchema)
async def get_job_by_id(
        job_id: str,
        container: Container = Depends(get_container),
) -> JobSchema:
    service: BaseJobService = container.resolve(BaseJobService)
    try:
        job = await service.get_job_by_id(job_id=job_id)
    except ApplicationException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message,
        )

    return JobSchema.from_entity(job)
