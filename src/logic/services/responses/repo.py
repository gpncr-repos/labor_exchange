from domain.entities.responses import ResponseEntity, ResponseAggregateJobEntity, ResponseAggregateUserEntity
from domain.entities.users import UserEntity
from infra.repositories.alchemy_models.responses import Response
from infra.repositories.jobs.base import BaseJobRepository
from infra.repositories.responses.base import BaseResponseRepository
from logic.exceptions.responses import OnlyNotCompanyUsersCanMakeResponsesException, ResponseDeleteLogicException, \
    OnlyCompanyCanGetJobResponses, OnlyJobOwnerCanGetJobResponsesException
from logic.services.responses.base import BaseResponseService


class RepositoryResponseService(BaseResponseService):
    def __init__(self, repository: BaseResponseRepository, job_repository: BaseJobRepository):
        self.repository = repository
        self.job_repository = job_repository

    async def make_response(self, response_in: ResponseEntity, user: UserEntity) -> ResponseEntity:
        if user.is_company:
            raise OnlyNotCompanyUsersCanMakeResponsesException
        new_response = await self.repository.add(response_in=response_in)
        return new_response.to_entity()

    async def get_user_response_list(
            self, user: UserEntity
    ) -> list[ResponseAggregateJobEntity] | list[ResponseAggregateUserEntity]:
        if user.is_company:
            response_list: list[Response] = await self.repository.get_list_by_company_user_id(user_id=user.id)
            return [response.to_aggregate_user_entity() for response in response_list]
        response_list: list[Response] = await self.repository.get_list_by_user_id(user_id=user.id)
        return [response.to_aggregate_job_entity() for response in response_list]

    async def get_job_response_list(self, job_id: str, user: UserEntity) -> list[ResponseEntity]:
        if not user.is_company:
            raise OnlyCompanyCanGetJobResponses
        job = await self.job_repository.get_one_by_id(job_id=job_id)
        if job.user_id != user.id:
            raise OnlyJobOwnerCanGetJobResponsesException
        response_list = await self.repository.get_list_by_user_id(user_id=user.id)
        return [response.to_detail_entity() for response in response_list]

    async def delete_response(self, response_id, user: UserEntity) -> None:
        response_to_delete: Response = await self.repository.get_one_by_id_join_job(response_id=response_id)
        if response_to_delete.job.user_id != user.id and response_to_delete.user_id != user.id:
            raise ResponseDeleteLogicException
        return await self.repository.delete(response_id=response_id)
