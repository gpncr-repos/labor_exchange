from abc import ABC
from dataclasses import dataclass

from core.security import verify_password, create_access_token
from domain.entities.users import UserEntity, TokenEntity
from infra.repositories.users.base import BaseUserRepository


@dataclass
class RepositoryUserService(ABC):
    repository: BaseUserRepository

    async def get_user_list(self, limit: int, offset: int) -> list[UserEntity]:
        return await self.repository.get_all(limit=limit, offset=offset)

    async def create_user(self, user_in: UserEntity) -> UserEntity:
        return await self.repository.add(user_in=user_in)

    async def update_user(self, user_id: int, user_in: UserEntity) -> UserEntity:
        return await self.repository.update(user_id=user_id, user_in=user_in)

    async def login_user(self, email: str, password: str):
        user = await self.repository.get_by_email(email=email)

        if user is None or not verify_password(password, user.hashed_password):
            raise Exception("Wrong creds")

        return TokenEntity(access_token=create_access_token({"sub": user.email}), token_type="Bearer")
