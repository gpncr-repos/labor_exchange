from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from domain.entities.users import UserEntity
from infra.repositories.alchemy_models.users import User
from infra.repositories.users.base import BaseUserRepository
from infra.repositories.users.converters import convert_user_entity_to_dto


class AlchemyUserRepository(BaseUserRepository):
    session: AsyncSession

    async def get_by_id(self, user_id: int) -> User:
        query = select(User).where(User.id == id).limit(1)
        res = await self.session.execute(query)
        return res.scalars().first()

    async def get_by_email(self, email: str) -> User:
        query = select(User).where(User.email == email).limit(1)
        res = await self.session.execute(query)
        return res.scalars().first()

    async def get_all(self, limit: int, offset: int) -> list[User]:
        query = select(User).limit(limit).offset(offset)
        res = await self.session.execute(query)
        return res.scalars().all()

    async def add(self, user_in: UserEntity) -> User:
        new_user = convert_user_entity_to_dto(user_in)
        self.session.add(new_user)
        await self.session.commit()
        await self.session.refresh(new_user)
        return new_user

    async def update(self, user_id: int, user_in: UserEntity) -> User:
        upd_user = convert_user_entity_to_dto(user_in)
        upd_user.id = user_id
        self.session.add(upd_user)
        await self.session.commit()
        await self.session.refresh(upd_user)
        return upd_user

    async def delete(self, user_id: int) -> None:
        user_to_delete = self.get_by_id(user_id)
        await self.session.delete(user_to_delete)
        await self.session.commit()
