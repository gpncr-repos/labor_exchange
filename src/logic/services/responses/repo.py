from domain.entities.responses import ResponseEntity, ResponseDetailEntity
from domain.entities.users import UserEntity
from infra.repositories.responses.base import BaseResponseRepository
from logic.exceptions.responses import OnlyNotCompanyUsersCanMakeResponsesException
from logic.services.responses.base import BaseResponseService


class RepositoryResponseService(BaseResponseService):
    def __init__(self, repository: BaseResponseRepository):
        self.repository = repository

    async def make_response(self, response_in: ResponseEntity, user: UserEntity) -> ResponseEntity:
        if user.is_company:
            raise OnlyNotCompanyUsersCanMakeResponsesException
        new_response = await self.repository.add(response_in=response_in)
        return new_response.to_entity()

    async def get_response_list_by_user_id(self, user_id) -> list[ResponseDetailEntity]:
        response_list = await self.repository.get_list_by_user_id(user_id=user_id)
        return [response.to_detail_entity() for response in response_list]
