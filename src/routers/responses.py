from typing import List

from fastapi import APIRouter, Depends, Form, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import get_current_employee, get_current_employer, get_db
from models import User
from queries import jobs as jobs_queries
from queries import responses as responses_queries
from schemas import ResponseInSchema, ResponseJobSchema

router = APIRouter(prefix="/responses", tags=["responses"])


@router.get("/{job_id}", response_model=List[ResponseJobSchema])
async def get_all_response_by_job_id(
    db: AsyncSession = Depends(get_db),
    job_id: int = Query(...),
    current_employer: User = Depends(get_current_employer),
):

    current_job = await jobs_queries.get_job_by_id(db=db, job_id=job_id)
    if not current_job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Вакансия не найдена"
        )
    elif not current_job.user_id == current_employer.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Недостаточно прав для просмотра откликов по вакансии",
        )

    return await responses_queries.get_response_by_user_id(db=db, job_id=job_id)


@router.post("/{job_id}", response_model=ResponseJobSchema)
async def send_response_to_job(
    db: AsyncSession = Depends(get_db),
    job_id: int = Query(...),
    message: str = Form(...),
    current_user: User = Depends(get_current_employee),
):

    current_job = await jobs_queries.get_job_by_id(db=db, job_id=job_id)
    if not current_job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Вакансия не найдена"
        )

    new_response = ResponseInSchema(
        user_id=current_user.id, job_id=job_id, message=message
    )
    return await responses_queries.response_job(db=db, response_schema=new_response)
