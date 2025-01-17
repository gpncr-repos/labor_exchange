from contextlib import AbstractContextManager
from typing import Callable

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from interfaces import IRepositoryAsync
from models import Job as JobModel
from models import Response as ResponseModel
from models import User as UserModel
from storage.sqlalchemy.tables import Response
from web.schemas import ResponseCreateSchema, ResponseUpdateSchema


class ResponseRepository(IRepositoryAsync):
    def __init__(self, session: Callable[..., AbstractContextManager[Session]]):
        self.session = session

    async def create(self, response_create_dto: ResponseCreateSchema) -> ResponseModel:
        async with self.session() as session:
            response = Response(
                id=response_create_dto.id,
                job_id=response_create_dto.job_id,
                user_id=response_create_dto.user_id,
                message=response_create_dto.message,
            )

            session.add(response)
            await session.commit()
            await session.refresh(response)

        return self.__to_response_model(response_from_db=response, include_relations=False)

    async def retrieve(self, include_relations: bool = False, **kwargs) -> ResponseModel:
        async with self.session() as session:
            query = select(Response).filter_by(**kwargs).limit(1)
            if include_relations:
                query = query.options(selectinload(Response.user)).options(selectinload(Response.job))

            res = await session.execute(query)
            response_from_db = res.scalars().first()

        response_model = self.__to_response_model(
            response_from_db=response_from_db, include_relations=include_relations
        )
        return response_model

    async def retrieve_many(
        self, limit: int = 100, skip: int = 0, include_relations: bool = False
    ) -> list[ResponseModel]:
        async with self.session() as session:
            query = select(Response).limit(limit).offset(skip)
            if include_relations:
                query = query.options(selectinload(Response.user)).options(selectinload(Response.job))

            res = await session.execute(query)
            responses_from_db = res.scalars().all()

        response_models = []
        for response in responses_from_db:
            model = self.__to_response_model(response_from_db=response, include_relations=include_relations)
            response_models.append(model)

        return response_models

    async def update(self, id: int, response_update_dto: ResponseUpdateSchema) -> ResponseModel:
        async with self.session() as session:
            query = select(Response).filter_by(id=id).limit(1)
            res = await session.execute(query)
            response_from_db = res.scalars().first()

            if not response_from_db:
                raise ValueError("Вакансия не найдена")

            job_id = response_update_dto.job_id if response_update_dto.job_id is not None else response_from_db.job_id
            user_id = response_update_dto.user_id if response_update_dto.user_id is not None else response_from_db.user_id
            message = response_update_dto.message if response_update_dto.message is not None else response_update_dto.message

            response_from_db.job_id = job_id
            response_from_db.user_id = user_id
            response_from_db.message = message

            session.add(response_from_db)
            await session.commit()
            await session.refresh(response_from_db)

        return self.__to_response_model(response_from_db, include_relations=False)

    async def delete(self, id: int) -> ResponseModel: # ???
        async with self.session() as session:
            query = select(Response).filter_by(id=id).limit(1)
            res = await session.execute(query)
            response_from_db = res.scalars().first()

            if response_from_db:
                await session.delete(response_from_db)
                await session.commit()
            else:
                raise ValueError("Вакансия не найдена")

        return self.__to_response_model(response_from_db, include_relations=False)

    @staticmethod
    def __to_response_model(response_from_db: Response, include_relations: bool = False) -> ResponseModel:
        response_job = None
        response_user = None
        response_model = None

        if response_from_db:
            if include_relations:
                response_job = response_from_db.job
                response_user = response_from_db.user

            response_model = ResponseModel(
                id=response_from_db.id,
                job_id=response_from_db.job_id,
                user_id=response_from_db.user_id,
                message=response_from_db.message,
            )

        return response_model
