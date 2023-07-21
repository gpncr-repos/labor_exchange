from unittest.mock import MagicMock

import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from db_settings import SQLALCHEMY_DATABASE_URL
from dependencies import get_db
from factories.jobs import JobFactory
from factories.responses import ResponseFactory
from factories.users import UserFactory
from main import app
from core.security import create_token


@pytest_asyncio.fixture()
async def current_user(sa_session, request):
    if not hasattr(request, "param") or request.param == "anonymous":
        return
    if request.param == "user":
        user = UserFactory.build(is_company=False)
    elif request.param == "company":
        user = UserFactory.build(is_company=True)
    else:
        raise ValueError(f"Invalid param ({request.param}) for current_user fixture!")
    sa_session.add(user)
    await sa_session.commit()
    await sa_session.refresh(user)
    return user


@pytest_asyncio.fixture()
async def auth_token(current_user):
    if not current_user:
        return
    return create_token({"sub": current_user.email})


@pytest_asyncio.fixture()
async def client_app(sa_session, auth_token):
    app.dependency_overrides[get_db] = lambda: sa_session

    headers = {"Authorization": f"Bearer {auth_token}"} if auth_token else {}
    async with AsyncClient(app=app, base_url="http://test", headers=headers) as client:
        yield client


@pytest_asyncio.fixture()
async def sa_session():
    engine = create_async_engine(SQLALCHEMY_DATABASE_URL) # You must provide your database URL.
    connection = await engine.connect()
    trans = await connection.begin()

    Session = sessionmaker(connection, expire_on_commit=False, class_=AsyncSession)
    session = Session()

    session.commit = MagicMock(side_effect=session.flush)

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
