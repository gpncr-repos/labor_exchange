"""Классы для работы с таблицами в базе"""
from abc import ABC, abstractmethod
from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import Job, Response as VacancyResponse

ALL_RECORDS = 123456
ZERO = 0


class RepoAbs(ABC):
    """Абстрактный класс, объединяющий методы для работы с таблицей базы"""

    @abstractmethod
    async def add(self):
        raise NotImplementedError("Должен быть реализован метод добавления записи в таблицу")

    @abstractmethod
    async def get_all(self, limit: int = 100, skip: int = 0):
        raise NotImplementedError("Должен быть реализован метод получения всех записей из таблицы")

    @abstractmethod
    async def get_by_id(self, id: int):
        raise NotImplementedError("Должен быть реализован метод получения записи из таблицы по идентифиактору")


class RepoConcrete(RepoAbs):
    """Класс, где реализуются общие методы работы с таблицами create, update"""
    def __init__(self, db: AsyncSession, model = None):  # , model):
        self.model = model
        self.session = db

    async def add(self, model):
        self.session.add(model)
        await self.session.commit()
        await self.session.refresh(model)

    async def get_all(self, limit: int = ALL_RECORDS, skip: int = ZERO):
        query = select(self.model).limit(limit).offset(skip)
        res = await self.session.execute(query)
        return res.scalars().all()

    async def get_by_id(self, model_id: int):
        query = select(self.model).where(self.model.id==model_id).limit(1)
        res = await self.session.execute(query)
        return res.scalars().first()


class RepoJob(RepoConcrete):
    """Класс для работы с таблицей вакансий jobs"""
    def __init__(self, db: AsyncSession):
        super().__init__(db, Job)


class RepoUser(RepoConcrete):
    """Класс для работы с таблицей users"""

    def __init__(self, db: AsyncSession):
        super().__init__(db, VacancyResponse)


class RepoResponse(RepoConcrete):
    """Класс для работы с таблицей отлкликов responses"""
    def __init__(self, db: AsyncSession):
        super().__init__(self.session, VacancyResponse)

    async def get_responses_by_job_id(self, db: AsyncSession, job_id: int):
        """Возвращает отклики на заданную вакансию"""
        query = select(self.model).where(self.model.job_id==job_id)
        res = await db.execute(query)
        return res.scalars().all_or_none()
