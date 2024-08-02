import punq
from sqlalchemy.ext.asyncio import AsyncSession

from functools import lru_cache

from infra.repositories.alchemy_settings import get_session
from infra.repositories.jobs.alchemy import AlchemyJobRepository
from infra.repositories.jobs.base import BaseJobRepository
from infra.repositories.responses.alchemy import AlchemyResponseRepository
from infra.repositories.responses.base import BaseResponseRepository
from infra.repositories.users.alchemy import AlchemyUserRepository
from infra.repositories.users.base import BaseUserRepository
from logic.services.jobs.base import BaseJobService
from logic.services.jobs.repo import RepositoryJobService
from logic.services.responses.base import BaseResponseService
from logic.services.responses.repo import RepositoryResponseService
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
    container.register(BaseJobRepository)
    container.register(AlchemyJobRepository)
    container.register(BaseResponseRepository)
    container.register(AlchemyResponseRepository)

    # init services
    def init_sqlalchemy_user_service():
        repository: BaseUserRepository = container.resolve(AlchemyUserRepository)
        return RepositoryUserService(repository=repository)

    def init_sqlalchemy_job_service():
        repository: BaseJobRepository = container.resolve(AlchemyJobRepository)
        return RepositoryJobService(repository=repository)

    def init_sqlalchemy_response_service():
        repository: BaseResponseRepository = container.resolve(AlchemyResponseRepository)
        return RepositoryResponseService(repository=repository)

    container.register(BaseUserService, factory=init_sqlalchemy_user_service)
    container.register(BaseJobService, factory=init_sqlalchemy_job_service)
    container.register(BaseResponseService, factory=init_sqlalchemy_response_service)

    return container
