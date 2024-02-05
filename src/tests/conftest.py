import asyncio
import os

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from tests.fixtures.users import UserFactory
from fastapi.testclient import TestClient
from main import app
import pytest
import pytest_asyncio
from unittest.mock import MagicMock
from db_settings import SQLALCHEMY_DATABASE_URL

DB_T_USER = os.environ.get("DB_USER", "admin")
DB_T_PASS = os.environ.get("DB_PASS", "admin")
DB_T_HOST = os.environ.get("DB_HOST", "localhost")
DB_T_PORT = os.environ.get("DB_PORT", "5434")
DB_T_NAME = os.environ.get("DB_NAME", "labor-exchange")

SQLALCHEMY_TEST_DATABASE_URL = f"postgresql+asyncpg://{DB_T_USER}:{DB_T_PASS}@{DB_T_HOST}:{DB_T_PORT}/{DB_T_NAME}"


@pytest.fixture()
def client_app():
    client = TestClient(app)
    return client


@pytest_asyncio.fixture()
async def sa_session():
    # engine = create_async_engine(SQLALCHEMY_DATABASE_URL) # You must provide your database URL.
    engine = create_async_engine(SQLALCHEMY_TEST_DATABASE_URL)  # You must provide your database URL.
    connection = await engine.connect()
    trans = await connection.begin()

    Session = sessionmaker(connection, expire_on_commit=False, class_=AsyncSession)
    session = Session()

    async def mock_delete(instance):
        session.expunge(instance)
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
