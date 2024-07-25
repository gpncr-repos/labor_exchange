import asyncio

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from fixtures.users import UserFactory
from fixtures.jobs import JobFactory
from fastapi.testclient import TestClient
from main import app
import pytest
import pytest_asyncio
from unittest.mock import MagicMock
from db_settings import SQLALCHEMY_DATABASE_URL


@pytest.fixture()
def client_app():
    client = TestClient(app)
    return client


@pytest_asyncio.fixture()
async def sa_session():
    engine = create_async_engine(SQLALCHEMY_DATABASE_URL,echo=True) # You must provide your database URL.
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
    JobFactory.session = sa_session
    UserFactory.session = sa_session
    
