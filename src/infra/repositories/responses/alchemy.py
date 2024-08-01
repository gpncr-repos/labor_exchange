from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from domain.entities.responses import ResponseEntity
from infra.exceptions.base import RepositoryException
from infra.repositories.alchemy_models.jobs import Job
from infra.repositories.alchemy_models.responses import Response
from infra.repositories.alchemy_models.users import User
from infra.repositories.responses.base import BaseResponseRepository
from infra.repositories.responses.converters import convert_response_entity_to_dto


class AlchemyResponseRepository(BaseResponseRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, response_in: ResponseEntity) -> Response:
        new_response = convert_response_entity_to_dto(response_in)
        async with self.session as session:
            try:
                session.add(new_response)
                await session.commit()
            except IntegrityError:
                raise RepositoryException
        return new_response

    async def get_list_by_user_id(self, user_id: str) -> list[Response]:
        user_query = select(User).where(User.id == user_id)
        res_query = await self.session.execute(user_query)
        user = res_query.scalar_one()
        if not user.is_company:
            query = select(Response).where(Response.user_id == user_id).options(
                selectinload(Response.job)
            )
        else:
            query = select(Response).join(Job).filter(Job.user_id == user_id)
        async with self.session as session:
            res = await session.execute(query)
        return res.scalars()
