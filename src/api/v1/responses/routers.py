from fastapi import APIRouter, Depends, HTTPException, status

from api.dependencies.responses import get_response_service
from api.v1.jobs.schemas import JobSchema
from api.v1.responses.schemas import ResponseSchema, ResponseCreateSchema, ResponseDetailSchema
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


@router.get("", response_model=list[ResponseDetailSchema])
async def get_all_user_responses(
        user_id: str,
        response_service: BaseResponseService = Depends(get_response_service),
) -> list[ResponseDetailSchema]:
    try:
        responses = await response_service.get_response_list_by_user_id(user_id=user_id)
    except ApplicationException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e.message,
        )
    return [ResponseDetailSchema.from_entity(response) for response in responses]
