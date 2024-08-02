from domain.entities.users import UserEntity
from logic.services.users.base import BaseUserService
from logic.utils.auth import hash_password
from logic.exceptions.users import UpdateOtherUserException
from infra.repositories.alchemy_models.users import User as UserDTO
from infra.repositories.users.base import BaseUserRepository


class RepositoryUserService(BaseUserService):
    def __init__(self, repository: BaseUserRepository):
        self.repository = repository

    async def get_user_list(self, limit: int, offset: int) -> list[UserEntity]:
        user_list: list[UserDTO] = await self.repository.get_all(limit=limit, offset=offset)
        return [user.to_entity() for user in user_list]

    async def get_user_by_email(self, email: str) -> UserEntity:
        user = await self.repository.get_one_by_email(email=email)
        return user.to_entity()

    async def create_user(self, user_in: UserEntity) -> UserEntity:
        hashed_password = hash_password(user_in.password)
        user_in.hashed_password = hashed_password
        new_user: UserDTO = await self.repository.add(user_in=user_in)
        return new_user.to_entity()

    async def update_user(self, user_id: str, auth_user_email: str, user_in: UserEntity) -> UserEntity:
        old_user = await self.repository.get_one_by_id(user_id=user_id)
        if old_user.email != auth_user_email:
            raise UpdateOtherUserException(user_email=old_user.email)

        user_in.hashed_password = old_user.hashed_password
        user_in.id = user_id

        updated_user: UserDTO = await self.repository.update(user_in=user_in)
        return updated_user.to_entity()
