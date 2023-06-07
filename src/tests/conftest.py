import asyncio

from sqlalchemy import inspect
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from httpx import AsyncClient

from core.security import create_access_token
from dependencies import get_db
from fixtures.jobs import JobFactory
from fixtures.responses import ResponseFactory
from fixtures.users import UserFactory
from fastapi.testclient import TestClient
from main import app
import pytest
import pytest_asyncio
from unittest.mock import MagicMock
from db_settings import SQLALCHEMY_DATABASE_URL
from schemas import TokenSchema


@pytest_asyncio.fixture()
async def sa_session():
    engine = create_async_engine(SQLALCHEMY_DATABASE_URL)  # Создается асинхронный движок для подключения к базе данных
    connection = await engine.connect()  # Создается асинхронное соединение  с базой данных.
    trans = await connection.begin()  # Создается транзакция, которая представляет собой логическую группу операций, выполняемых над базой данных.

    Session = sessionmaker(connection, expire_on_commit=False, class_=AsyncSession)  # Класс для создания сессии
    session = Session()  # объект этого класса

    deletion = session.delete

    async def mock_delete(instance):
        insp = inspect(instance)  # содержит информацию о состоянии объекта
        if not insp.persistent:  # проверка, не является ли он сохранённым в базе данных
            session.expunge(instance)  # вызывается для удаления объекта из сессии
        else:
            await deletion(instance)  # вызывается для удаления объекта из базы данных

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


@pytest_asyncio.fixture()
async def company_user(sa_session: AsyncSession):
    new_user = UserFactory.build()
    new_user.is_company = True
    sa_session.add(new_user)

    await sa_session.commit()
    await sa_session.refresh(new_user)

    return new_user


@pytest_asyncio.fixture()
async def client_user(sa_session: AsyncSession):
    new_user = UserFactory.build()
    new_user.is_company = False
    sa_session.add(new_user)

    await sa_session.commit()
    await sa_session.refresh(new_user)

    return new_user


@pytest_asyncio.fixture()
async def http_client(sa_session: AsyncSession, access_token: TokenSchema):
    app.dependency_overrides[get_db] = lambda: sa_session

    async with AsyncClient(app=app, base_url="http://test") as client:
        client.headers["Authorization"] = f"Bearer {access_token.access_token}"
        yield client

@pytest_asyncio.fixture()
async def undefined_user(sa_session: AsyncSession):
    new_user = UserFactory.build()
    sa_session.add(new_user)

    await sa_session.commit()
    await sa_session.refresh(new_user)

    return new_user
@pytest_asyncio.fixture()
async def access_token(undefined_user):
    token = TokenSchema(
        access_token=create_access_token({"sub": undefined_user.email}),
        token_type="Bearer"
    )
    return token


# регистрация фабрик
@pytest_asyncio.fixture(autouse=True)
def setup_factories(sa_session: AsyncSession) -> None:
    UserFactory.session = sa_session
    JobFactory.session = sa_session
    ResponseFactory.session = sa_session
