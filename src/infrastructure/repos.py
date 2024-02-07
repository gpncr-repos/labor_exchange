"""Классы для работы с таблицами в базе"""
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional

from dataclass_factory import Factory
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import EmailStr

from core.security import hash_password
from domain.do_schemas import DOJob, DOUser, DOResponse
from models import Job, Response as VacancyResponse, User

RECORDS_NUM = 100
ZERO = 0

factory = Factory()

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
        sa_objs = res.scalars().all()
        # result = list()
        # for sa_obj in sa_objs:
        #     dm_obj = DOJob(
        #         user_id=sa_obj.user_id,
        #         title=sa_obj.title,
        #         description=sa_obj.description,
        #         salary_from=sa_obj.salary_from,
        #         salary_to=sa_obj.salary_to,
        #         is_active=sa_obj.is_active,
        #         created_at=sa_obj.created_at,
        #     )
        #     result.append(dm_obj)

        return sa_objs


    async def get_by_id(self, model_id: int):
        query = select(Job).where(Job.id==model_id).limit(1)
        res = await self.session.execute(query)
        orm_obj = res.scalars().first()
        # dm_obj = factory.load(sa_obj, DOJob)
        # dm_obj = DOJob(
        #     user_id=orm_obj.user_id,
        #     title=orm_obj.title,
        #     description=orm_obj.description,
        #     salary_from=orm_obj.salary_from,
        #     salary_to=orm_obj.salary_to,
        #     is_active=orm_obj.is_active,
        #     created_at=orm_obj.created_at,
        # )
        return orm_obj

    async def update(self, job_to_update: Job) -> Job:
        await self.session.merge(job_to_update)
        await self.session.commit()
        await self.session.refresh(job_to_update)
        return job_to_update

    async def del_by_id(self, obj_to_del_id: int):
        query = select(Job).filter(Job.id==obj_to_del_id).limit(1)
        res = await self.session.execute(query)
        job_to_del = res.scalars().first()
        await self.session.delete(job_to_del)
        await self.session.commit()
        return obj_to_del_id

class RepoUser(RepoAbs):
    """Класс для работы с таблицей users"""

    def __init__(self, db: AsyncSession):
        self.session = db

    async def add(self, obj_to_add):
        user = User(
            name=obj_to_add.name,
            email=obj_to_add.email,
            hashed_password=hash_password(obj_to_add.password),
            is_company=obj_to_add.is_company,
            # created_at=datetime.utcnow(),
        )
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        # obj_to_add.id = user.id
        return user

    async def get_by_id(self, model_id: int):
        query = select(User).where(User.id==model_id).limit(1)
        res = await self.session.execute(query)
        orm_obj = res.scalars().first()
        # dm_obj = DOUser(
        #     id=sa_obj.id,
        #     email=sa_obj.email,
        #     name=sa_obj.name,
        #     hashed_password=sa_obj.hashed_password,
        #     is_company=sa_obj.is_company,
        #     created_at=sa_obj.created_at,
        # )
        return orm_obj

    async def get_all(self, limit: int = RECORDS_NUM, skip: int = ZERO):
        query = select(User).limit(limit).offset(skip)
        res = await self.session.execute(query)
        orm_objs = res.scalars().all()
        return orm_objs

    async def update(self, user: User) -> DOUser:  # User:
        await self.session.merge(user)
        await self.session.commit()
        await self.session.refresh(user)
        user_do = DOUser(
            id=user.id,
            email=user.email,
            name=user.name,
            hashed_password=user.hashed_password,
            is_company=user.is_company,
            created_at=user.created_at,
        )
        return user_do

    async def get_by_email(self, email: EmailStr) -> User:
        stmt = select(User).where(User.email==email).limit(1)
        res = await self.session.execute(stmt)
        orm_obj = res.scalars().first()
        # dm_obj = DOUser(
        #     id=orm_obj_obj.id,
        #     email=orm_obj.email,
        #     name=orm_obj.name,
        #     hashed_password=orm_obj.hashed_password,
        #     is_company=orm_obj.is_company,
        #     created_at=orm_obj.created_at,
        # )
        return orm_obj

class RepoResponse(RepoAbs):
    """Класс для работы с таблицей откликов responses"""
    def __init__(self, db: AsyncSession):
        self.session = db
        self.model = VacancyResponse

    async def add(self, obj_to_add):
        sa_obj_to_add = VacancyResponse(
            user_id=obj_to_add.user_id,
            job_id=obj_to_add.job_id,
            message=obj_to_add.message,
        )
        self.session.add(sa_obj_to_add)
        await self.session.commit()
        await self.session.refresh(sa_obj_to_add)
        obj_to_add.id = sa_obj_to_add.id
        return obj_to_add

    async def get_all(self, limit: int = RECORDS_NUM, skip: int = ZERO):
        query = select(VacancyResponse).limit(limit).offset(skip)
        res = await self.session.execute(query)
        sa_objs = res.scalars().all()
        result = list()
        for sa_obj in sa_objs:
            dm_obj = DOResponse(
                id=sa_obj.id,
                user_id=sa_obj.user_id,
                job_id=sa_obj.job_id,
                message=sa_obj.message,
            )
        return result

    async def get_by_id(self, model_id: int):
        query = select(VacancyResponse).where(VacancyResponse==model_id).limit(1)
        res = await self.session.execute(query)
        sa_obj = res.scalars().first()
        dm_obj = DOResponse(
            id=sa_obj.id,
            user_id=sa_obj.user_id,
            job_id=sa_obj.job_id,
            message=sa_obj.message,
        )
        return dm_obj

    async def del_by_id(self, obj_to_del_id: int):
        stmt = delete(VacancyResponse).where(VacancyResponse.id==obj_to_del_id)
        await self.session.execute(stmt)
        await self.session.commit()

    async def get_resps_by_job_id(self, db: AsyncSession, job_id: int):
        """Возвращает отклики на заданную вакансию"""
        query = select(VacancyResponse).where(VacancyResponse.job_id==job_id)
        res = await db.execute(query)
        orm_objs = res.scalars().all()
        return orm_objs

# async def get_resps_by_job_id(db: AsyncSession, job_id: int):
#     """Возвращает отклики на заданную вакансию"""
#     query = select(VacancyResponse).where(VacancyResponse.job_id==job_id)
#     res = await db.execute(query)
#     return res.scalars().all()
