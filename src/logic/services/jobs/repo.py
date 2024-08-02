from domain.entities.jobs import JobEntity
from domain.entities.users import UserEntity
from infra.exceptions.base import RepositoryException
from infra.repositories.alchemy_models.jobs import Job as JobDTO
from infra.repositories.jobs.base import BaseJobRepository
from logic.exceptions.jobs import (OnlyCompanyCanCreateJobException, OnlyCompanyCanDeleteJobException,
                                   OnlyJobOwnerCanDeleteJobException)
from logic.services.jobs.base import BaseJobService


class RepositoryJobService(BaseJobService):
    def __init__(self, repository: BaseJobRepository):
        self.repository = repository

    async def get_job_by_id(self, job_id: str):
        job = await self.repository.get_one_by_id(job_id=job_id)
        return job.to_entity()

    async def get_job_list(self, limit: int, offset: int) -> list[JobEntity]:
        job_list: list[JobDTO] = await self.repository.get_all(limit=limit, offset=offset)
        return [job.to_entity() for job in job_list]

    async def create_job(self, job_in: JobEntity, auth_user: UserEntity):
        if not auth_user.is_company:
            raise OnlyCompanyCanCreateJobException
        new_job = await self.repository.add(job_in=job_in)
        return new_job.to_entity()

    async def delete_job(self, job_id: str, user: UserEntity) -> None:
        if not user.is_company:
            raise OnlyCompanyCanDeleteJobException
        job_to_delete: JobDTO = await self.repository.get_one_by_id(job_id=job_id)
        if job_to_delete.user_id != user.id:
            raise OnlyJobOwnerCanDeleteJobException
        await self.repository.delete(job_id=job_id)
