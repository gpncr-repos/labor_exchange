import punq
from sqlalchemy.ext.asyncio import AsyncSession

from functools import lru_cache

from infra.repositories.alchemy_settings import get_session
from infra.repositories.users.alchemy import AlchemyUserRepository
from infra.repositories.users.base import BaseUserRepository
from logic.services.users.base import BaseUserService
from logic.services.users.repo import RepositoryUserService


@lru_cache(1)
def get_container() -> punq.Container:
    return _initialize_container()


def _initialize_container() -> punq.Container:
    container = punq.Container()

    # init session
    container.register(AsyncSession, factory=get_session)

    # init repos
    container.register(BaseUserRepository)
    container.register(AlchemyUserRepository)

    # init services
    def init_sqlalchemy_user_service():
        repository: BaseUserRepository = container.resolve(AlchemyUserRepository)
        return RepositoryUserService(repository=repository)

    container.register(BaseUserService, factory=init_sqlalchemy_user_service)

    return container
