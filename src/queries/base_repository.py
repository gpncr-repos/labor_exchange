from abc import ABC, abstractmethod
from typing import Type, List, Optional, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete

from db_settings import Base


class AbstractAsyncRepository(ABC):
    """Интерфейс запросов в бд"""
    model: Type[Base]

    @abstractmethod
    async def get_list(
            self,
            db: AsyncSession,
            limit: int = 100,
            skip: int = 0,
            *args_filters,
            **kwargs_filters,

    ) -> List["AbstractAsyncRepository.model"]:
        pass

    @abstractmethod
    async def get_single(self, db: AsyncSession, *args, **kwargs) -> Optional["AbstractAsyncRepository.model"]:
        pass

    @abstractmethod
    async def delete(self, db: AsyncSession, *args, **kwargs) -> None:
        pass

    @abstractmethod
    async def create(
            self,
            db: AsyncSession,
            instance: "AbstractAsyncRepository.model"
    ) -> "AbstractAsyncRepository.model":
        pass

    @abstractmethod
    async def update(
            self,
            db: AsyncSession,
            instance: "AbstractAsyncRepository.model"
    ) -> "AbstractAsyncRepository.model":
        pass

    @staticmethod
    async def _get_scalars(db: AsyncSession, query: Any):
        res = await db.execute(query)
        return res.scalars()

    @staticmethod
    async def _commit_instance(db: AsyncSession, instance: Any):
        db.add(instance)
        await db.commit()
        await db.refresh(instance)
        return instance


class BaseAsyncRepository(AbstractAsyncRepository, ABC):
    """Общая реализация запросов к бд"""
    async def get_list(
            self,
            db: AsyncSession,
            limit: int = 100,
            skip: int = 0,
            *args_filters,
            **kwargs_filters
    ) -> List["AbstractAsyncRepository.model"]:
        query = select(self.model).filter(*args_filters).filter_by(**kwargs_filters).limit(limit).offset(skip)
        scalars = await self._get_scalars(db, query)
        return scalars.all()

    async def get_single(self, db: AsyncSession, *args, **kwargs) -> Optional["AbstractAsyncRepository.model"]:
        query = select(self.model).filter(*args).filter_by(**kwargs).limit(1)
        scalars = await self._get_scalars(db, query)
        return scalars.first()

    async def create(
            self,
            db: AsyncSession,
            instance: "AbstractAsyncRepository.model"
    ) -> "AbstractAsyncRepository.model":
        return await self._commit_instance(db, instance)

    async def update(
            self,
            db: AsyncSession,
            instance: "AbstractAsyncRepository.model"
    ) -> "AbstractAsyncRepository.model":
        return await self._commit_instance(db, instance)

    async def delete(self, db: AsyncSession, *args, **kwargs) -> None:
        query = delete(self.model).filter(*args).filter_by(**kwargs)
        await db.execute(query)
