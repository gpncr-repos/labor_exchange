from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from schemas import ResponsesSchema,ResponsestoSchema,ResponsesinSchema
from dependencies import get_db, get_current_user
from sqlalchemy.ext.asyncio import AsyncSession
from queries import responses as responses_queries
from queries import jobs as jobs_queries
from models import User
router = APIRouter(prefix="/responses", tags=["responses"])

@router.get("/responses_job_id/{job_id}", response_model=list[ResponsesSchema])
async def get_responses_by_job_id(
    job_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
    ):
    """
    Выдача откликов по job_ID:
    job_id: ID вакансии
    db: коннект к базе данных
    current_user: текущий пользователь
    """
    if current_user.is_company:
        res=await responses_queries.get_response_by_job_id(db=db, job_id=job_id)
    else:
        res=await responses_queries.get_response_by_job_id_and_user_id(db=db,job_id=job_id,user_id=current_user.id)
    if len(res)==0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Окликов нет")
    return res

@router.get("/responses_user_id/{user_id}", response_model=list[ResponsesSchema])
async def get_responses_by_user_id(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
    ):
    """
    Выдача откликов по user_id:
    job_id: ID вакансии
    db: коннект к базе данных
    current_user: текущий пользователь
    """
    if not current_user.is_company:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Выдача откликов по пользователям доступна только не компаниям")
    res=await responses_queries.get_response_by_user_id(db=db, user_id=user_id)
    if len(res)==0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Окликов нет")
    return res

@router.post("", response_model=ResponsestoSchema)
async def create_response(
    response:ResponsesinSchema,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)):
    """
    Создание отклика:
    response: данные для создания отклика согласно схемы ResponsestoSchema
    db: коннект к базе данных
    current_user: текущий пользователь
    """
    if current_user.is_company:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Пользователь является компанией")
    is_double_responce=await responses_queries.get_response_by_job_id_and_user_id(db=db,job_id=response.job_id,user_id=current_user.id)
    if is_double_responce:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Отклик уже есть")
    is_active_job=await jobs_queries.get_by_id(db=db,id=response.job_id)
    if not is_active_job:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Нет такой вакансии")
    if not is_active_job.is_active:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Вакансия не активна")
    try:
        res = await responses_queries.response_create(db=db, response_schema=response,user_id=current_user.id)
    except Exception:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Нет такого пользователя или вакансии")
    return ResponsestoSchema.from_orm(res)

@router.patch("/patch_response/{job_id}", response_model=ResponsesSchema)
async def patch_response(
    job_id:int,
    response:ResponsesinSchema,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)):
    """
    Изменение отклика:
    job_id: id вакансии для изменения
    response: данные для создания отклика согласно схемы ResponsesSchema
    db: коннект к базе данных
    current_user: текущий пользователь
    """
    responce_from_db=await responses_queries.get_response_by_job_id_and_user_id(db=db,job_id=job_id,user_id=current_user.id)
    if not responce_from_db:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Отклика от текущего пользователя на эту вакансию нет")
    is_active_job=(await jobs_queries.get_by_id(db=db,id=job_id)).is_active
    if not is_active_job:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Вакансия не активна")
    new_response=ResponsesSchema
    new_response=responce_from_db
    new_response.massage = new_response.massage if response.massage is not None else responce_from_db.massage
    res = await responses_queries.update(db=db, response=new_response)
    return ResponsestoSchema.from_orm(res)

@router.delete("/patch_response/{job_id}")
async def delete_response(
    job_id:int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)):
    """
    Удаление отклика:
    job_id: id вакансии для изменения
    db: коннект к базе данных
    current_user: текущий пользователь
    """
    responce_from_db=await responses_queries.get_response_by_job_id_and_user_id(db=db,job_id=job_id,user_id=current_user.id)
    if not responce_from_db:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Отклика от текущего пользователя на эту вакансию нет")
    is_active_job=await jobs_queries.get_by_id(db=db,id=job_id)
    if not is_active_job.is_active:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Вакансия не активна")
    res = await responses_queries.delete(db=db,response=responce_from_db)
    return res