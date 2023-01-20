import asyncio

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import inspect

from core.security import create_access_token
from dependencies import get_db
from fixtures.jobs import JobFactory
from fixtures.responses import ResponseFactory
from fixtures.users import UserFactory
from main import app
import pytest_asyncio
from httpx import AsyncClient
from unittest.mock import MagicMock
from db_settings import SQLALCHEMY_DATABASE_URL
from schemas import TokenSchema
from queries import UserRepository, JobRepository, ResponseRepository


@pytest_asyncio.fixture()
async def sa_session():
    engine = create_async_engine(SQLALCHEMY_DATABASE_URL)  # You must provide your database URL.
    connection = await engine.connect()
    trans = await connection.begin()

    Session = sessionmaker(connection, expire_on_commit=False, class_=AsyncSession)
    session = Session()

    deletion = session.delete

    async def mock_delete(instance):

        insp = inspect(instance)
        if not insp.persistent:
            session.expunge(instance)
        else:
            await deletion(instance)
        return await asyncio.sleep(0)

    session.commit = MagicMock(side_effect=session.flush)
    session.delete = MagicMock(side_effect=mock_delete)

    try:
        yield session
    finally:
        await session.close()
        await trans.rollback()
        await connection.close()
        await engine.dispose()


# регистрация фабрик
@pytest_asyncio.fixture(autouse=True)
def setup_factories(sa_session: AsyncSession) -> None:
    UserFactory.session = sa_session
    JobFactory.session = sa_session
    ResponseFactory.session = sa_session


@pytest_asyncio.fixture()
async def user_repo():
    return UserRepository()


@pytest_asyncio.fixture()
async def job_repo():
    return JobRepository()


@pytest_asyncio.fixture()
async def response_repo():
    return ResponseRepository()


@pytest_asyncio.fixture()
async def current_user(sa_session: AsyncSession):
    new_user = UserFactory.build()
    sa_session.add(new_user)

    await sa_session.commit()
    await sa_session.refresh(new_user)

    return new_user


@pytest_asyncio.fixture()
async def access_token(current_user):
    token = TokenSchema(
        access_token=create_access_token(dict(sub=current_user.email)),
        token_type="Bearer"
    )
    return token


@pytest_asyncio.fixture()
async def client_app(sa_session: AsyncSession, access_token: TokenSchema):
    app.dependency_overrides[get_db] = lambda: sa_session

    async with AsyncClient(app=app, base_url="http://test") as client:
        client.headers["Authorization"] = f"{access_token.token_type} {access_token.access_token}"

        yield client
