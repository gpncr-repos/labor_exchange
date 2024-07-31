from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from domain.entities.responses import ResponseEntity
from infra.repositories.alchemy_models.responses import Response
from infra.repositories.responses.base import BaseResponseRepository
from infra.repositories.responses.converters import convert_response_entity_to_dto


class AlchemyResponseRepository(BaseResponseRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, response_in: ResponseEntity) -> Response:
        new_response = convert_response_entity_to_dto(response_in)
        async with self.session as session:
            session.add(new_response)
            await session.commit()
        return new_response

    async def get_list_by_user_id(self, user_id: str) -> list[Response]:
        query = select(Response).where(Response.user_id == user_id).options(
            selectinload(Response.job)
        )
        async with self.session as session:
            res = await session.execute(query)
        return res.scalars()
