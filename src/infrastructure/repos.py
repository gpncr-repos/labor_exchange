"""Классы для работы с таблицами в базе"""
from abc import ABC, abstractmethod
from typing import Optional
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from models import Job, Response as VacancyResponse, User

ALL_RECORDS = 123456
ZERO = 0


class RepoAbs(ABC):
    """Абстрактный класс, объединяющий методы для работы с таблицей базы"""
    model = None

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
    def __init__(self, db: AsyncSession):    #, model = None):  # , model):
        self.model = None
        self.session = db

    async def add(self, obj_to_add):

        self.session.add(obj_to_add)
        await self.session.commit()
        await self.session.refresh(obj_to_add)
        return obj_to_add

    async def get_all(self, limit: int = ALL_RECORDS, skip: int = ZERO):
        query = select(self.model).limit(limit).offset(skip)
        res = await self.session.execute(query)
        result = res.scalars().all()
        return result


    async def get_by_id(self, model_id: int):
        query = select(self.model).where(self.model.id==model_id).limit(1)
        res = await self.session.execute(query)
        result = res.scalars().first()
        return result


    async def del_by_id(self, obj_to_del_id: int):
        stmt = delete(self.model).where(id==obj_to_del_id)
        await self.session.execute(stmt)
        await self.session.commit()

class RepoJob(RepoConcrete):
    """Класс для работы с таблицей вакансий jobs"""
    def __init__(self, db: AsyncSession):
        self.session = db
        self.model = Job

    async def del_by_id(self, obj_to_del_id: int, author_id):
        """Удаляет вакансию, если это делает автор этой вакансии"""
        # query = select(Job).filter(Job.id==job_id, Job.user_id==author_id).limit(1)
        # res = await db.execute(query)
        query = select(self.model).filter(self.model.id==obj_to_del_id, self.model.user_id==author_id).limit(1)
        res = await self.session.execute(query)
        obj_to_del = res.scalar()
        if obj_to_del:
            await self.session.delete(obj_to_del)
            await self.session.commit()
            return obj_to_del_id

class RepoUser(RepoConcrete):
    """Класс для работы с таблицей users"""

    def __init__(self, db: AsyncSession):
        self.session = db
        self.model = User


class RepoResponse(RepoConcrete):
    """Класс для работы с таблицей отлкликов responses"""
    def __init__(self, db: AsyncSession):
        self.session = db
        self.model = VacancyResponse

    async def get_responses_by_job_id(self, db: AsyncSession, job_id: int):
        """Возвращает отклики на заданную вакансию"""
        query = select(self.model).where(job_id==job_id)
        res = await db.execute(query)
        return res.scalars().all_or_none()

async def get_resps_by_job_id(db: AsyncSession, job_id: int):
    """Возвращает отклики на заданную вакансию"""
    query = select(VacancyResponse).where(VacancyResponse.job_id==job_id)
    res = await db.execute(query)
    return res.scalars().all()
