from abc import ABC, abstractmethod

from domain.entities.users import UserEntity


class BaseJobService(ABC):
    @abstractmethod
    async def get_job_by_id(self, job_id: str):
        ...

    @abstractmethod
    async def get_job_list(self, limit: int, offset: int):
        ...

    @abstractmethod
    async def create_job(self, job_in, auth_user: UserEntity):
        ...

    @abstractmethod
    async def delete_job(self, job_id: str, user: UserEntity) -> None:
        ...
