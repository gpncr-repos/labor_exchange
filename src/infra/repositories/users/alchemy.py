from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from domain.entities.users import UserEntity
from infra.exceptions.users import UserAlreadyExistsDBException, UserNotFoundDBException
from infra.repositories.alchemy_models.users import User
from infra.repositories.users.base import BaseUserRepository
from infra.repositories.users.converters import convert_user_entity_to_dto


class AlchemyUserRepository(BaseUserRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, user_id: str) -> User:
        query = select(User).where(User.id == user_id).limit(1)
        async with self.session as session:
            try:
                res = await session.execute(query)
                user = res.scalar_one()
            except NoResultFound:
                raise UserNotFoundDBException(user_id=user_id)
        return user

    async def get_by_email(self, email: str) -> User:
        query = select(User).where(User.email == email).limit(1)
        async with self.session as session:
            try:
                res = await session.execute(query)
                user = res.scalar_one()
            except NoResultFound:
                raise UserNotFoundDBException(user_email=email)
        return user

    async def get_all(self, limit: int, offset: int) -> list[User]:
        query = select(User).limit(limit).offset(offset)
        async with self.session as session:
            res = await session.execute(query)
        return res.scalars().all()

    async def add(self, user_in: UserEntity) -> User:
        new_user = convert_user_entity_to_dto(user_in)
        async with self.session as session:
            try:
                session.add(new_user)
                await session.commit()
                await session.refresh(new_user)
            except IntegrityError:
                raise UserAlreadyExistsDBException(user_email=user_in.email)
        return new_user

    async def update(self, user_in: UserEntity) -> User:
        async with self.session as session:
            query = update(User).where(User.id == user_in.id).values(
                **user_in.to_not_nullable_values_dict()
            ).returning(User)
            try:
                res = await session.execute(query)
                await session.commit()
            except IntegrityError:
                raise UserAlreadyExistsDBException(user_email=user_in.email)
        return res.scalars().first()

    async def delete(self, user_id: str) -> None:
        user_to_delete = self.get_by_id(user_id)
        async with self.session as session:
            await session.delete(user_to_delete)
            await session.commit()
