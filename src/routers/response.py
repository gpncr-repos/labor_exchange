from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from schemas import ResponseSchema, ResponseCreateSchema, ResponseInSchema
from dependencies import get_db, get_current_user
from sqlalchemy.ext.asyncio import AsyncSession
from queries import response as response_queries
from models import User


router = APIRouter(prefix="/responses", tags=["responses"])


@router.get("/{job_id}", response_model=List[ResponseSchema])
async def get_response_by_job_id(job_id: int, db: AsyncSession = Depends(get_db)):
    return await response_queries.get_by_job_id(db=db, job_id=job_id)


@router.post("", response_model=ResponseSchema)
async def response_job(
    response_schema: ResponseInSchema,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.is_company:
        raise HTTPException(
            status_code=403, detail="Откликаться на вакансию могут только соискатели"
        )
    response_create_schema = ResponseCreateSchema(
        user_id=current_user.id,
        job_id=response_schema.job_id,
        message=response_schema.message,
    )
    response = await response_queries.create(
        db=db, response_schema=response_create_schema
    )
    return ResponseSchema.from_orm(response)
