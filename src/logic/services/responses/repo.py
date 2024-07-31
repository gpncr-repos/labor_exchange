from domain.entities.responses import ResponseEntity
from infra.repositories.responses.base import BaseResponseRepository
from logic.services.responses.base import BaseResponseService


class RepositoryResponseService(BaseResponseService):
    def __init__(self, repository: BaseResponseRepository):
        self.repository = repository

    async def make_response(self, response_in: ResponseEntity) -> ResponseEntity:
        #TODO только пользователь НЕКОМПАНИЯ может делать отклик
        #TODO только один отклик на одну вакансию у пользавателя
        new_response = await self.repository.add(response_in=response_in)
        return new_response.to_entity()

    async def get_response_list_by_user_id(self, user_id) -> list[ResponseEntity]:
        response_list = await self.repository.get_list_by_user_id(user_id=user_id)
        return [response.to_entity() for response in response_list]
