import pytest

from domain.entities.users import UserEntity
from infra.exceptions.users import UserAlreadyExistsDBException
from infra.repositories.users.alchemy import AlchemyUserRepository
from tests.repositories.fixtures import UserFactory


@pytest.mark.asyncio
async def test_get_all(sa_session):
    user = UserFactory.build()
    sa_session.add(user)
    await sa_session.flush()

    repo = AlchemyUserRepository(sa_session)
    all_users = await repo.get_all(limit=100, offset=0)
    assert all_users
    assert user in all_users


@pytest.mark.asyncio
async def test_get_by_id(sa_session):
    user = UserFactory.build()
    sa_session.add(user)
    await sa_session.flush()

    repo = AlchemyUserRepository(sa_session)
    current_user = await repo.get_by_id(user.id)
    assert current_user is not None
    assert current_user.id == user.id


@pytest.mark.asyncio
async def test_get_by_email(sa_session):
    user = UserFactory.build()
    sa_session.add(user)
    await sa_session.flush()

    repo = AlchemyUserRepository(sa_session)
    current_user = await repo.get_by_email(user.email)
    assert current_user is not None
    assert current_user.id == user.id


@pytest.mark.asyncio
async def test_create(sa_session):
    user = UserEntity(
        name="Uchpochmak",
        email="bashkort@example.com",
        hashed_password="eshkere!",
        is_company=False
    )

    repo = AlchemyUserRepository(sa_session)
    new_user = await repo.add(user_in=user)
    assert new_user is not None
    assert new_user.name == "Uchpochmak"
    assert new_user.hashed_password == "eshkere!"


@pytest.mark.asyncio
async def test_update(sa_session):
    user = UserFactory.build()
    sa_session.add(user)
    await sa_session.flush()

    repo = AlchemyUserRepository(sa_session)
    entity = user.to_entity()
    entity.name = "updated_name"
    updated_user = await repo.update(user_in=entity)
    assert user.id == updated_user.id
    assert updated_user.name == "updated_name"


@pytest.mark.asyncio
async def test_create_same_email_error(sa_session):
    user = UserEntity(
        name="Uchpochmak",
        email="bashkort@example.com",
        hashed_password="eshkere!",
        is_company=False
    )

    repo = AlchemyUserRepository(sa_session)
    await repo.add(user_in=user)
    with pytest.raises(UserAlreadyExistsDBException):
        await repo.add(user_in=user)
