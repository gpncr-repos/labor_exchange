from abc import abstractmethod, ABC

from domain.entities.users import UserEntity


class BaseUserService(ABC):

    @abstractmethod
    async def get_user_list(self, limit: int, offset: int) -> list[UserEntity]:
        ...

    @abstractmethod
    async def create_user(self, user_in: UserEntity) -> UserEntity:
        ...

    @abstractmethod
    async def update_user(self, user_id: str, auth_user_email: str, user_in: UserEntity) -> UserEntity:
        ...

    @abstractmethod
    async def login_user(self, email: str, password: str):
        ...
