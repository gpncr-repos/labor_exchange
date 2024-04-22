import asyncio
from unittest.mock import MagicMock

import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from core.security import create_access_token
from db_settings import SQLALCHEMY_DATABASE_URL
from dependencies import get_db
from fixtures.jobs import JobFactory
from fixtures.responses import ResponseFactory
from fixtures.users import UserFactory
from main import app
from schemas import UserSchema


@pytest_asyncio.fixture()
async def user(sa_session, request):
    if not hasattr(request, "param") or request.param == "unauthorized":
        return None
    new_user = UserFactory.build()
    if request.param == "company":
        new_user.is_company = True
    elif request.param == "user":
        new_user.is_company = False

    sa_session.add(new_user)
    await sa_session.commit()
    await sa_session.refresh(new_user)
    return new_user


@pytest_asyncio.fixture()
async def authorization_token(user: UserSchema):
    return None if user is None else create_access_token({"sub": user.email})


@pytest_asyncio.fixture()
async def client_app(sa_session, authorization_token):
    app.dependency_overrides[get_db] = lambda: sa_session
    headers = (
        {"Authorization": f"Bearer {authorization_token}"}
        if authorization_token is not None
        else {}
    )

    async with AsyncClient(app=app, base_url="http://test", headers=headers) as client:
        yield client


@pytest_asyncio.fixture()
async def sa_session():
    engine = create_async_engine(SQLALCHEMY_DATABASE_URL)
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
    JobFactory.session = sa_session
    ResponseFactory.session = sa_session
