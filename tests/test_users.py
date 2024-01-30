import pytest
from queries import user as user_query
from fixtures.users import UserFactory
from schemas import UserInSchema
from pydantic import ValidationError


@pytest.mark.asyncio
async def test_get_all(sa_session):
    user = UserFactory.build()
    sa_session.add(user)
    sa_session.flush()

    all_users = await user_query.get_all(sa_session)
    assert all_users
    assert len(all_users) == 1
    assert all_users[0] == user


@pytest.mark.asyncio
async def test_get_by_id(sa_session):
    user = UserFactory.build()
    sa_session.add(user)
    sa_session.flush()

    current_user = await user_query.get_by_id(sa_session, user.id)
    assert current_user is not None
    assert current_user.id == user.id


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
    user = UserInSchema(
        name="Uchpochmak",
        email="bashkort@example.com",
        password="eshkere!",
        password2="eshkere!",
        is_company=False
    )

    new_user = await user_query.create(sa_session, user_schema=user)
    assert new_user is not None
    assert new_user.name == "Uchpochmak"
    assert new_user.hashed_password != "eshkere!"


@pytest.mark.asyncio
async def test_create_password_mismatch(sa_session):
    with pytest.raises(ValidationError):
        user = UserInSchema(
            name="Uchpochmak",
            email="bashkort@example.com",
            password="eshkere!",
            password2="eshkero!",
            is_company=False
        )
        await user_query.create(sa_session, user_schema=user)


@pytest.mark.asyncio
async def test_update(sa_session):
    user = UserFactory.build()
    sa_session.add(user)
    sa_session.flush()

    user.name = "updated_name"
    updated_user = await user_query.update(sa_session, user=user)
    assert user.id == updated_user.id
    assert updated_user.name == "updated_name"
