import asyncio
import os
import pytest_asyncio
from unittest.mock import MagicMock

from sqlalchemy import inspect
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from httpx import AsyncClient

import models
from api.schemas import TokenSchema
from applications.dependencies import get_db
from applications.dependencies.db import get_repo_job
from core.security import create_access_token
from infrastructure.repos import RepoJob
from tests.fixtures.factories import UserFactory, JobFactory, ResponseFactory #, EmployerFactory, EmployeeFactory
from main import app

DB_T_USER = os.environ.get("DB_USER", "admin")
DB_T_PASS = os.environ.get("DB_PASS", "admin")
DB_T_HOST = os.environ.get("DB_HOST", "localhost")
DB_T_PORT = os.environ.get("DB_PORT", "5434")
DB_T_NAME = os.environ.get("DB_NAME", "labor-exchange")

SQLALCHEMY_TEST_DATABASE_URL = f"postgresql+asyncpg://{DB_T_USER}:{DB_T_PASS}@{DB_T_HOST}:{DB_T_PORT}/{DB_T_NAME}"


@pytest_asyncio.fixture()
async def sa_session():
    engine = create_async_engine(SQLALCHEMY_TEST_DATABASE_URL) # You must provide your database URL.
    connection = await engine.connect()
    trans = await connection.begin()

    Session = sessionmaker(connection, expire_on_commit=False, class_=AsyncSession, info={
        "what_A_session": "session_for_tests"})
    session = Session()

    deletion = session.delete
    async def mock_delete(instance):
        insp = inspect(instance)
        if not insp.persistent:
            session.expunge(instance)
        else:
            await deletion(instance)

        return await asyncio.sleep(0)

    refreshing = session.refresh
    async def mock_refresh(instance):
        # insp = inspect(instance)
        # if not insp.persistent:
        #     session.flush(instance)
        # else:
        #     await refreshing(instance)

        return await asyncio.sleep(0)

    # закомментировал этот мок, т.к. из-за отсутствия пользователя в базе не удавалось добавить вакансию от его имени
    session.commit = MagicMock(side_effect=session.flush)
    session.delete = MagicMock(side_effect=mock_delete)
    # session.refresh = MagicMock(side_effect=session.flush)
    # session.refresh = MagicMock(side_effect=mock_refresh)

    try:
        yield session
    finally:
        await session.close()
        await trans.rollback()
        await connection.close()
        await engine.dispose()

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
        token=create_access_token({"sub": current_user.email}),
        token_type="Bearer"
    )
    return token

@pytest_asyncio.fixture()
async def test_job(sa_session: AsyncSession, current_user: models.User):
    test_job = JobFactory.build()
    sa_session.add(current_user)
    sa_session.flush()
    sa_session.commit()
    return test_job


# регистрация фабрик
@pytest_asyncio.fixture(autouse=True)
def setup_factories(sa_session: AsyncSession) -> None:
    UserFactory.session = sa_session
    # EmployeeFactory.session = sa_session
    # EmployerFactory.session = sa_session
    JobFactory.session = sa_session
    ResponseFactory.session = sa_session


@pytest_asyncio.fixture()
async def client_app(sa_session: AsyncSession, access_token: TokenSchema):
    app.dependency_overrides[get_db] = lambda: sa_session
    app.dependency_overrides[get_repo_job] = lambda: RepoJob(sa_session)

    async with AsyncClient(app=app, base_url="http://test") as client:
        client.headers["Authorization"] = f"Bearer {access_token.token}"
        yield client
