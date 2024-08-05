from abc import ABC, abstractmethod

from domain.entities.responses import ResponseEntity
from domain.entities.users import UserEntity


class BaseResponseService(ABC):

    @abstractmethod
    async def make_response(self, response_in: ResponseEntity, user: UserEntity):
        ...

    @abstractmethod
    async def get_user_response_list(self, user: UserEntity):
        ...

    @abstractmethod
    async def get_job_response_list(self, job_id: str, user: UserEntity):
        ...

    @abstractmethod
    async def delete_response(self, response_id: str, user: UserEntity):
        ...
