from abc import ABC, abstractmethod

from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from labor_exchange.db_settings import SessionLocal
from labor_exchange.src.domain.models.jobs import Job
from labor_exchange.src.domain.models.users import User
from labor_exchange.src.domain.models.responses import Response as VacancyResponse


ALL_RECORDS = 123456
ZERO = 0

class RepoAbs(ABC):
    """Класс объединяет методы для работы с таблицей базы"""

    def __init__(self): #, model):
        self.model = None
    
    @abstractmethod
    async def add(self, db: AsyncSession, schema):
        raise NotImplementedError("Должен быть реализован метод добавления записи в таблицу")
    
    @abstractmethod
    async def get_all(self, db: AsyncSession, limit: int=100, skip: int = 0):
        raise NotImplementedError("Должен быть реализован метод получения всех записей из таблицы")
    
    
    @abstractmethod
    async def get_by_id(self, db: AsyncSession, id: int):
        raise NotImplementedError("Должен быть реализован метод получения записи из таблицы по идентифиактору")

class RepoConcrete(ABC):

    async def add(self, db: AsyncSession, schema):
        async with db as session:
            await session.add(schema)
            await session.commit()

    async def get_all(self, db: AsyncSession, limit: int = ALL_RECORDS, skip: int = ZERO)
        async with db as session:
            result = await session.scalars(select(self.model).skip(skip).limit(limit))
            return result

    async def get_by_id(self, db: AsyncSession, model_id: int):
        async with db as session:
            result = await session.scalars(select(self.model).filter_by(id=model_id))
            return result

class RepoJob(RepoConcrete):
    
    def __init__(self):
        self.model = Job

    async def create_job(self, db: AsyncSession, job_schema):
        # async with db as session:
        #     ins_query = insert(self.model).values(job_schema).returning(self.model.id)
        #     id = await session.execute(ins_query)
        #     return id
        result = await super().add(db, job_schema)
    
    async def get_all_jobs(self, db: AsyncSession, limit: int = 100, skip: int = 0):
        # async with db as session:
        #     query = select(self.model).skip(skip).limit(limit)
        #     result = await session.execute(query)
        #     return result.all_or_none()
        result = await super().get_all(db, limit, skip)
        return result
        
    async def get_job_by_id(self, db: AsyncSession, job_id: int):
        async with db as session:
            # query = select(self.model).filter_by(id=job_id)
            # result = await session.execute(query)
            # return result.all_or_none()
            result = await super().get_by_id(db, job_id)

class RepoUser(RepoConcrete):
    """Класс для работы с таблицей Users"""
    def __init__(self):
        self.model = User


class RepoResponse(RepoConcrete):
    model = VacancyResponse

    async def get_response_by_user_id(db: AsyncSession, job_id: int):
        async with db as session:
            result = session.scalars(select(self.model).filter_by(id=job_id))
    