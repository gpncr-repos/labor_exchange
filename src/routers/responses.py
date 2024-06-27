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
async def read_all_responses(
    db: AsyncSession = Depends(get_db),
    limit: int = 100,
    skip: int = 0):
    return await responses_queries.get_all_responses(db=db, limit=limit, skip=skip)


@router.post("", response_model=ResponseSchema)
async def create_job(
    user_id: int,
    job_id: int,
    message: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)):

    old_user = await user_queries.get_by_id(db=db, id=user_id)

    if old_user is None or old_user.email != current_user.email:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь не найден")
    if old_user.is_company == True:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Вы работодатель. Вам нельзя откликаться на вакансии")

    old_job = await jobs_queries.get_job_by_id(db=db, job_id=job_id)
    if old_job is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Работа не найдена")

    new_response = await responses_queries.response_job(db=db, user_id=user_id, job_id=job_id, message=message)
    return ResponseSchema.from_orm(new_response)
