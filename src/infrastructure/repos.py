"""Классы для работы с таблицами в базе"""
from abc import ABC, abstractmethod
from typing import Optional
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import EmailStr

from models import Job, Response as VacancyResponse, User

RECORDS_NUM = 100
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


# class RepoConcrete(RepoAbs):
#     """Класс, где реализуются общие методы работы с таблицами create, update"""
#     model = None
#     def __init__(self, db: AsyncSession):    #, model = None):  # , model):
#         self.session = db
#
#     async def add(self, obj_to_add):
#
#         self.session.add(obj_to_add)
#         await self.session.commit()
#         await self.session.refresh(obj_to_add)
#         return obj_to_add
#
#     async def get_all(self, limit: int = ALL_RECORDS, skip: int = ZERO):
#         query = select(self.model).limit(limit).offset(skip)
#         res = await self.session.execute(query)
#         result = res.scalars().all()
#         return result
#
#
#     async def get_by_id(self, model_id: int):
#         query = select(self.model).where(__class__.model.id==model_id).limit(1)
#         # query = select(self.model).where(User.id==model_id).limit(1)
#         # query = select(User).where(User.id==model_id).limit(1)
#         res = await self.session.execute(query)
#         result = res.scalars().first()
#         return result
#
#
#     async def del_by_id(self, obj_to_del_id: int):
#         stmt = delete(self.model).where(id==obj_to_del_id)
#         await self.session.execute(stmt)
#         await self.session.commit()

class RepoJob(RepoAbs):
    """Класс для работы с таблицей вакансий jobs"""
    def __init__(self, db: AsyncSession):
        self.session = db

    async def add(self, obj_to_add):

        self.session.add(obj_to_add)
        await self.session.commit()
        await self.session.refresh(obj_to_add)
        return obj_to_add

    async def get_all(self, limit: int = RECORDS_NUM, skip: int = ZERO):
        query = select(Job).limit(limit).offset(skip)
        res = await self.session.execute(query)
        result = res.scalars().all()
        return result


    async def get_by_id(self, model_id: int):
        query = select(Job).where(Job.id==model_id).limit(1)
        res = await self.session.execute(query)
        result = res.scalars().first()
        return result

    # async def del_by_id(self, obj_to_del_id: int, author_id):
    #     """Удаляет вакансию по запросу автора этой вакансии"""
    #     # query = select(Job).filter(Job.id==job_id, Job.user_id==author_id).limit(1)
    #     # res = await db.execute(query)
    #     query = select(Job).filter(Job.id==obj_to_del_id, Job.user_id==author_id).limit(1)
    #     res = await self.session.execute(query)
    #     obj_to_del = res.scalar()
    #     if obj_to_del:
    #         await self.session.delete(obj_to_del)
    #         await self.session.commit()
    #         return obj_to_del_id

    async def del_by_id(self, obj_to_del_id: int):
        query = select(Job).filter(Job.id==obj_to_del_id).limit(1)
        res = await self.session.execute(query)
        job_to_del = res.scalars().first()
        await self.session.delete(job_to_del)
        await self.session.commit()
        return obj_to_del_id
        # return CommandResult.success(result="Вакансия %s удалена" % job_id)
        # await delete(Job).where(Job.id==obj_to_del_id)
        # await self.session.execute(stmt)
        # await self.session.commit()

class RepoUser(RepoAbs):
    """Класс для работы с таблицей users"""

    def __init__(self, db: AsyncSession):
        self.session = db

    async def add(self, obj_to_add):

        self.session.add(obj_to_add)
        await self.session.commit()
        await self.session.refresh(obj_to_add)
        return obj_to_add

    async def get_by_id(self, model_id: int):
        query = select(User).where(User.id==model_id).limit(1)
        res = await self.session.execute(query)
        result = res.scalars().first()
        return result

    async def get_all(self, limit: int = RECORDS_NUM, skip: int = ZERO):
        query = select(User).limit(limit).offset(skip)
        res = await self.session.execute(query)
        result = res.scalars().all()
        return result

    async def update(self, user: User):  # User:
        await self.session.merge(user)  # add(user) # TODO: check, debug
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def get_by_email(self, email: EmailStr) -> User:
        stmt = select(User).where(User.email==email).limit(1)
        res = await self.session.execute(stmt)
        return res.scalars().first()

class RepoResponse(RepoAbs):
    """Класс для работы с таблицей отлкликов responses"""
    def __init__(self, db: AsyncSession):
        self.session = db
        self.model = VacancyResponse

    async def add(self, obj_to_add):

        self.session.add(obj_to_add)
        await self.session.commit()
        await self.session.refresh(obj_to_add)
        return obj_to_add

    async def get_all(self, limit: int = RECORDS_NUM, skip: int = ZERO):
        query = select(VacancyResponse).limit(limit).offset(skip)
        res = await self.session.execute(query)
        result = res.scalars().all()
        return result

    async def get_by_id(self, model_id: int):
        query = select(VacancyResponse).where(VacancyResponse==model_id).limit(1)
        res = await self.session.execute(query)
        result = res.scalars().first()
        return result

    async def del_by_id(self, obj_to_del_id: int):
        stmt = delete(VacancyResponse).where(VacancyResponse.id==obj_to_del_id)
        await self.session.execute(stmt)
        await self.session.commit()

    async def get_resps_by_job_id(self, db: AsyncSession, job_id: int):
        """Возвращает отклики на заданную вакансию"""
        query = select(VacancyResponse).where(VacancyResponse.job_id==job_id)
        res = await db.execute(query)
        return res.scalars().all_or_none()

# async def get_resps_by_job_id(db: AsyncSession, job_id: int):
#     """Возвращает отклики на заданную вакансию"""
#     query = select(VacancyResponse).where(VacancyResponse.job_id==job_id)
#     res = await db.execute(query)
#     return res.scalars().all()
