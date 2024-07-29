from abc import ABC, abstractmethod


class BaseUserRepository(ABC):
    @abstractmethod
    async def get_by_id(self, user_id: int):
        ...

    @abstractmethod
    async def get_all(self, limit: int, offset: int):
        ...

    @abstractmethod
    async def add(self, user_in):
        ...

    @abstractmethod
    async def update(self, user_id: int, user_in):
        ...

    @abstractmethod
    async def delete(self, user_id: int):
        ...

    @abstractmethod
    async def get_by_email(self, email: str):
        ...
