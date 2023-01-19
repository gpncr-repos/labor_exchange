import pytest
from fixtures.users import UserFactory
from schemas import UserInSchema
from pydantic import ValidationError


@pytest.mark.asyncio
async def test_get_all(sa_session, user_repo):
    user = UserFactory.build()
    sa_session.add(user)
    sa_session.flush()

    all_users = await user_repo.get_list(sa_session)
    assert all_users
    assert len(all_users) == 1
    assert all_users[0] == user


@pytest.mark.asyncio
async def test_get_by_id(sa_session, user_repo):
    user = UserFactory.build()
    sa_session.add(user)
    sa_session.flush()

    current_user = await user_repo.get_single(sa_session, id=user.id)
    assert current_user is not None
    assert current_user.id == user.id


@pytest.mark.asyncio
async def test_get_by_email(sa_session, user_repo):
    user = UserFactory.build()
    sa_session.add(user)
    sa_session.flush()

    current_user = await user_repo.get_single(sa_session, email=user.email)
    assert current_user is not None
    assert current_user.id == user.id


@pytest.mark.asyncio
async def test_create(sa_session, user_repo):
    user = UserInSchema(
        name="Uchpochmak",
        email="bashkort@example.com",
        password="eshkere!",
        password2="eshkere!",
        is_company=False
    )

    new_user = await user_repo.create_by_schema(sa_session, user)
    assert new_user is not None
    assert new_user.name == "Uchpochmak"
    assert new_user.hashed_password != "eshkere!"


@pytest.mark.asyncio
async def test_create_password_mismatch(sa_session, user_repo):
    with pytest.raises(ValidationError):
        user = UserInSchema(
            name="Uchpochmak",
            email="bashkort@example.com",
            password="eshkere!",
            password2="eshkero!",
            is_company=False
        )
        await user_repo.create_by_schema(sa_session, user)


@pytest.mark.asyncio
async def test_update(sa_session, user_repo):
    user = UserFactory.build()
    sa_session.add(user)
    sa_session.flush()

    user.name = "updated_name"
    updated_user = await user_repo.update(sa_session, user)
    assert user.id == updated_user.id
    assert updated_user.name == "updated_name"
