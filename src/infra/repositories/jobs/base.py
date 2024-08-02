from abc import ABC, abstractmethod


class BaseJobRepository(ABC):
    @abstractmethod
    async def get_one_by_id(self, job_id: str):
        ...

    @abstractmethod
    async def get_all(self, limit: int, offset: int):
        ...

    @abstractmethod
    async def add(self, job_in):
        ...

    @abstractmethod
    async def delete(self, job_id: str):
        ...
