from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from schemas import ResponseSchema
from dependencies import get_db, get_current_user
from sqlalchemy.ext.asyncio import AsyncSession
from queries import user as user_queries
from queries import jobs as jobs_queries
from queries import responses as responses_queries
from models import User


router = APIRouter(prefix="/responses", tags=["responses"])


@router.get("", response_model=List[ResponseSchema])
async def read_all_my_responses(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)):

    if current_user.is_company is True:
        return await responses_queries.get_response_by_employer_id(db=db, user_id=current_user.id)
    return await responses_queries.get_response_by_user_id(db=db, user_id=current_user.id)

@router.post("", response_model=ResponseSchema)
async def response_job(
    job_id: int,
    message: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)):

    if current_user.is_company is True:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Вы работодатель. Вам нельзя откликаться на вакансии")

    job = await jobs_queries.get_job_by_id(db=db, job_id=job_id)
    if job is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Работа не найдена")
    if job.is_active is False:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Вакансия не является активной")
    new_response = await responses_queries.response_job(db=db, user_id=current_user.id, job_id=job_id, message=message)
    return ResponseSchema.from_orm(new_response)
