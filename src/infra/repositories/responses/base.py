from abc import ABC, abstractmethod

from domain.entities.responses import ResponseEntity


class BaseResponseRepository(ABC):

    @abstractmethod
    async def add(self, response_in: ResponseEntity):
        ...

    @abstractmethod
    async def get_list_by_user_id(self, user_id: str):
        ...
