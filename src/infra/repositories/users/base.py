from abc import ABC, abstractmethod


class BaseUserRepository(ABC):
    @abstractmethod
    async def get_one_by_id(self, user_id: str):
        ...

    @abstractmethod
    async def get_all(self, limit: int, offset: int):
        ...

    @abstractmethod
    async def add(self, user_in):
        ...

    @abstractmethod
    async def update(self, user_in):
        ...

    @abstractmeth
    async def get_one_by_email(self, email: str):
        ...
