from typing import List
from fastapi import APIRouter, Depends, HTTPException, status

from models import Job
from schemas.response import ResponseSchema, ResponseInSchema, ResponseUpdateSchema
from dependencies import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from queries import response as response_queries

router = APIRouter(prefix="/responses", tags=["responses"])


@router.get("", response_model=List[ResponseSchema])
async def read_responses(
        db: AsyncSession = Depends(get_db),
        job_id=Job.id):
    return await response_queries.get_response_by_job_id(db=db, job_id=job_id)


@router.post("", response_model=ResponseSchema)
async def create_job(response: ResponseInSchema, db: AsyncSession = Depends(get_db)):
    response = await response_queries.create_response(db=db, response_schema=response)
    return ResponseSchema.from_orm(response)


@router.put("", response_model=ResponseSchema)
async def update_response(
        id: int,
        response: ResponseUpdateSchema,
        db: AsyncSession = Depends(get_db)):

    old_response = await response_queries.get_response_by_job_id(db=db, job_id=id)

    if old_response is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Отклик не найден")

    old_response.message = response.message if response.message is not None else old_response.message

    new_response = await response_queries.update_response(db=db, response=old_response)

    return ResponseSchema.from_orm(new_response)
