from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from schemas import ResponsesSchema,ResponsestoSchema
from dependencies import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from queries import responses as responses_queries


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
    response:ResponsestoSchema,
    db: AsyncSession = Depends(get_db)):
    """
    Создание вакансии:
    job: данные для создания вакансии согласно схемы JobfromSchema
    db: коннект к базе данных
    """
    response = await responses_queries.response_create(db=db, response_schema=response)
    return ResponsestoSchema.from_orm(response)
