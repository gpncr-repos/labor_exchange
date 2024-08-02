from abc import ABC, abstractmethod

from domain.entities.responses import ResponseEntity


class BaseResponseRepository(ABC):

    @abstractmethod
    async def add(self, response_in: ResponseEntity):
        ...

    @abstractmethod
    async def get_one_by_id(self, response_id: str):
        ...

    @abstractmethod
    async def get_one_by_id_join_job(self, response_id: str):
        ...

    @abstractmethod
    async def get_list_by_user_id(self, user_id: str):
        ...

    @abstractmethod
    async def get_list_by_company_user_id(self, user_id: str):
        ...

    @abstractmethod
    async def delete(self, response_id: str):
        ...
