from abc import ABC, abstractmethod

from domain.entities.responses import ResponseEntity
from domain.entities.users import UserEntity


class BaseResponseService(ABC):

    @abstractmethod
    async def make_response(self, response_in: ResponseEntity, user: UserEntity):
        ...

    @abstractmethod
    async def get_response_list_by_user_id(self, user_id):
        ...
