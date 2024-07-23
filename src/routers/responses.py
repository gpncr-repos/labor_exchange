from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from schemas import ResponsesSchema,ResponsestoSchema,ResponsesinSchema
from dependencies import get_db, get_current_user
from sqlalchemy.ext.asyncio import AsyncSession
from queries import responses as responses_queries
from models import User
router = APIRouter(prefix="/responses", tags=["responses"])

@router.get("/job_id/{job_id}", response_model=ResponsesSchema)
async def get_responses_by_job_id(
    job_id: int,
    db: AsyncSession = Depends(get_db)
    ):
    """
    Выдача откликов по job_ID:
    job_id: ID вакансии
    db: коннект к базе данных
    """
    res=await responses_queries.get_response_by_job_id(db=db, job_id=job_id)
    if len(res)==0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Окликов нет")
    return res


@router.post("", response_model=ResponsestoSchema)
async def create_response(
    response_pr:ResponsesinSchema,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)):
    """
    Создание отклика:
    response: данные для создания отклика согласно схемы ResponsestoSchema
    db: коннект к базе данных
    """
    if current_user.is_company:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь является компанией")
    try:
        res = await responses_queries.response_create(db=db, response_schema=response_pr,user_id=current_user.id)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Нет такого пользователя или вакансии")

    return ResponsestoSchema.from_orm(res)
