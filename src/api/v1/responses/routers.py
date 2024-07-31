from fastapi import APIRouter, Depends

from api.dependencies.responses import get_response_service
from api.v1.jobs.schemas import JobSchema
from api.v1.responses.schemas import ResponseSchema
from api.dependencies.users import get_current_user
from domain.entities.users import UserEntity
from logic.services.responses.base import BaseResponseService

router = APIRouter(prefix="/responses", tags=["responses"])


@router.post("", response_model=ResponseSchema)
async def make_response(
        response: ResponseSchema,
        auth_user: UserEntity = Depends(get_current_user),
        response_service: BaseResponseService = Depends(get_response_service),
) -> list[JobSchema]:
    new_response = await response_service.make_response(response_in=response.to_entity())
    return new_response


@router.get("", response_model=list[ResponseSchema])
async def get_all_user_responses(
        user_id: str,
        response_service: BaseResponseService = Depends(get_response_service),
) -> list[ResponseSchema]:
    responses = await response_service.get_response_list_by_user_id(user_id=user_id)
    return [ResponseSchema.from_entity(response) for response in responses]
