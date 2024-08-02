from fastapi import APIRouter, Depends, HTTPException, status

from api.dependencies.responses import get_response_service
from api.v1.jobs.schemas import JobSchema
from api.v1.responses.schemas import ResponseSchema, ResponseCreateSchema, ResponseAggregateJobSchema, \
    ResponseAggregateUserSchema
from api.dependencies.users import get_current_user
from core.exceptions import ApplicationException
from domain.entities.users import UserEntity
from logic.services.responses.base import BaseResponseService

router = APIRouter(prefix="/responses", tags=["responses"])


@router.post("", response_model=ResponseSchema)
async def make_response(
        response: ResponseCreateSchema,
        auth_user: UserEntity = Depends(get_current_user),
        response_service: BaseResponseService = Depends(get_response_service),
) -> list[JobSchema]:
    response.user_id = auth_user.id
    try:
        new_response = await response_service.make_response(
            response_in=response.to_entity(),
            user=auth_user,
        )
    except ApplicationException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e.message,
        )
    return new_response


@router.get("/my_responses", response_model=list[ResponseAggregateJobSchema])
async def get_all_user_responses(
        auth_user: UserEntity = Depends(get_current_user),
        response_service: BaseResponseService = Depends(get_response_service),
) -> list[ResponseAggregateJobSchema] | list[ResponseAggregateUserSchema]:
    if auth_user.is_company:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Эндпоинт для получения откликов пользователя!",
        )
    try:
        responses = await response_service.get_user_response_list(user=auth_user)
    except ApplicationException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e.message,
        )
    return [ResponseAggregateJobSchema.from_entity(response) for response in responses]


@router.get("/my_company_responses", response_model=list[ResponseAggregateUserSchema])
async def get_all_company_responses(
        auth_user: UserEntity = Depends(get_current_user),
        response_service: BaseResponseService = Depends(get_response_service),
) -> list[ResponseAggregateJobSchema] | list[ResponseAggregateUserSchema]:
    if not auth_user.is_company:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Эндпоинт для получения откликов компаний!",
        )
    try:
        responses = await response_service.get_user_response_list(user=auth_user)
    except ApplicationException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e.message,
        )
    return [ResponseAggregateUserSchema.from_entity(response) for response in responses]


@router.get("/job_responses", response_model=list[ResponseAggregateUserSchema])
async def get_all_job_responses(
        job_id: str,
        auth_user: UserEntity = Depends(get_current_user),
        response_service: BaseResponseService = Depends(get_response_service),
) -> list[ResponseAggregateUserSchema]:
    try:
        responses = await response_service.get_job_response_list(job_id=job_id, user=auth_user)
    except ApplicationException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e.message,
        )
    return [ResponseAggregateUserSchema.from_entity(response) for response in responses]


@router.delete("", status_code=status.HTTP_204_NO_CONTENT)
async def delete_response(
        response_id: str,
        auth_user: UserEntity = Depends(get_current_user),
        response_service: BaseResponseService = Depends(get_response_service),
) -> None:
    try:
        await response_service.delete_response(response_id=response_id, user=auth_user)
    except ApplicationException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message,
        )
