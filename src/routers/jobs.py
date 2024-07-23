from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from schemas import JobSchema,JobtoSchema
from dependencies import get_db, get_current_user
from sqlalchemy.ext.asyncio import AsyncSession
from queries import jobs as jobs_queries
from models import Job


router = APIRouter(prefix="/jobs", tags=["jobs"])

@router.get("/{job_id}", response_model=JobSchema)
async def get_job_by_id(
    job_id: int,
    db: AsyncSession = Depends(get_db)
    ):
    """
    Выдача вакансии по ID:
    job_id: ID вакансии
    db: коннект к базе данных
    """
    res=await jobs_queries.get_by_id(db=db, id=job_id)
    if res is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Вакансия не найдена")
    return res



@router.get("", response_model=List[JobSchema])
async def get_all_jobs(
    db: AsyncSession = Depends(get_db),
    limit: int = 100,
    skip: int = 0):
    """
    Выдача вакансий по limit штук от skip:
    db: коннект к базе данных
    limit: кол-во записей для вывода,
    skip: от какой записи начинать вывод):
    """
    res=await jobs_queries.get_all(db=db, limit=limit, skip=skip)
    if len(res)==0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="В базе данных нет вакансий")
    return res


@router.post("", response_model=JobtoSchema)
async def create_job(
    job:JobtoSchema,
    db: AsyncSession = Depends(get_db)):
    """
    Создание вакансии:
    job: данные для создания вакансии согласно схемы JobfromSchema
    db: коннект к базе данных
    """
    job = await jobs_queries.create(db=db, job_schema=job)
    return JobtoSchema.from_orm(job)
