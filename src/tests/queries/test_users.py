import pytest

from fixtures.users import UserFactory
from queries import user as user_query
from schemas import UserCreateSchema


@pytest.mark.asyncio
async def test_get_all(sa_session):
    user_count = 10
    skip = 5
    limit = 8
    for _ in range(user_count):
        user = UserFactory.build()
        sa_session.add(user)
    sa_session.flush()
    all_users = await user_query.get_all(sa_session, limit=limit, skip=skip)

    assert len(all_users) == min(user_count - skip, limit)


@pytest.mark.asyncio
async def test_get_by_id(sa_session):
    user = UserFactory.build()
    sa_session.add(user)
    sa_session.flush()

    current_user = await user_query.get_by_id(sa_session, user.id)
    assert current_user is not None
    assert current_user.email == user.email


@pytest.mark.asyncio
async def test_get_by_email(sa_session):
    user = UserFactory.build()
    sa_session.add(user)
    sa_session.flush()

    current_user = await user_query.get_by_email(sa_session, user.email)
    assert current_user is not None
    assert current_user.id == user.id


@pytest.mark.asyncio
async def test_create(sa_session):
    user = UserCreateSchema(
        name="Uchpochmak",
        email="bashkort@example.com",
        password="eshkere!",
        password2="eshkere!",
        is_company=False,
    )

    new_user = await user_query.create(sa_session, user_schema=user)
    assert new_user is not None
    assert new_user.name == "Uchpochmak"
    assert new_user.hashed_password != "eshkere!"


@pytest.mark.asyncio
async def test_update(sa_session):
    user = UserFactory.build()
    sa_session.add(user)
    sa_session.flush()
    user.name = "update_name"
    user.email = "update_email"
    old_company = user.is_company
    user.is_company = not old_company
    updated_user = await user_query.update(sa_session, user=user)
    res = await user_query.get_by_id(sa_session, updated_user.id)
    assert res.name == "update_name"
    assert res.email == "update_email"
    assert res.is_company != old_company


@pytest.mark.asyncio
async def test_delete(sa_session):
    user = UserFactory.build()
    sa_session.add(user)
    sa_session.flush()

    delete_user = await user_query.delete(sa_session, delete_user=user)
    res = await user_query.get_by_id(sa_session, user.id)
    assert delete_user.id == user.id
    assert res is None
