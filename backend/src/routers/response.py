from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from queries import response as response_service
from dependencies import get_db, get_current_user
from models import User
from schemas.response import ResponseSchema, ResponseInSchema

router = APIRouter(prefix='/responses', tags=["responses"])


@router.post("", response_model=ResponseSchema)
async def create_response(
        created_response: ResponseInSchema,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    """
    Create a new response.

    - **created_response**: The response to be created.
    - **db**: Database session dependency.
    - **current_user**: Currently authenticated user dependency.
    - **Returns**: The created response.
    """
    created_response = await response_service.create_response(db=db, response_schema=created_response,
                                                              current_user=current_user)
    return ResponseSchema.from_orm(created_response)


@router.get("", response_model=List[ResponseSchema])
async def get_all_responses(db: AsyncSession = Depends(get_db)):
    """
    Get all responses.

    - **db**: Database session dependency.
    - **Returns**: List of all responses.
    """
    responses = await response_service.get_all_responses(db=db)
    return responses


@router.get("/job-id/{job_id}", response_model=List[ResponseSchema])
async def get_responses_by_job_id(
        job_id: int,
        db: AsyncSession = Depends(get_db)
):
    """
    Get a list of responses by job ID.

    - **job_id**: The job ID to retrieve responses for.
    - **db**: Database session dependency.
    - **Returns**: List of responses matching the job ID.
    """
    responses = await response_service.get_responses_by_job_id(db=db, job_id=job_id)
    return responses


@router.get("/user-id/{user_id}", response_model=List[ResponseSchema])
async def get_responses_by_user_id(
        user_id: int,
        db: AsyncSession = Depends(get_db)
):
    """
    Get a list of responses by user ID.

    - **user_id**: The user ID to retrieve responses for.
    - **db**: Database session dependency.
    - **Returns**: List of responses matching the user ID.
    """
    responses = await response_service.get_responses_by_user_id(db=db, user_id=user_id)
    return responses


@router.delete("/{response_id}", response_model=bool)
async def delete_response(
        response_id: int,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    """
    Delete a response by ID.

    - **response_id**: The ID of the response to delete.
    - **db**: Database session dependency.
    - **current_user**: Currently authenticated user dependency.
    - **Returns**: True if the response was successfully deleted, exception otherwise.
    """
    is_deleted = await response_service.delete_response_by_id(db, response_id=response_id, current_user=current_user)
    return is_deleted
