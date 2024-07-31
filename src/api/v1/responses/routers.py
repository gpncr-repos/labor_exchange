from fastapi import APIRouter, Depends

from api.dependencies.responses import get_response_service
from api.v1.jobs.schemas import JobSchema
from api.v1.responses.schemas import ResponseSchema, ResponseCreateSchema, ResponseDetailSchema
from api.dependencies.users import get_current_user
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
    new_response = await response_service.make_response(
        response_in=response.to_entity(),
        user=auth_user,
    )
    return new_response


@router.get("", response_model=list[ResponseDetailSchema])
async def get_all_user_responses(
        user_id: str,
        response_service: BaseResponseService = Depends(get_response_service),
) -> list[ResponseDetailSchema]:
    responses = await response_service.get_response_list_by_user_id(user_id=user_id)
    return [ResponseDetailSchema.from_entity(response) for response in responses]
