import pytest
from pydantic import ValidationError

from fixtures.users import UserFactory
from queries import user as user_query
from schemas import UserInSchema


@pytest.mark.asyncio
async def test_get_all(sa_session):
    all_users = await user_query.get_all(sa_session)
    coutUser = len(all_users)
    user = UserFactory.build()
    sa_session.add(user)
    user = UserFactory.build()
    sa_session.add(user)
    sa_session.flush()
    all_users = await user_query.get_all(sa_session)

    assert len(all_users) == coutUser + 2


@pytest.mark.asyncio
async def test_get_by_id(sa_session):
    user = UserFactory.build()
    sa_session.add(user)
    sa_session.flush()

    current_user = await user_query.get_by_id(sa_session, user.id)
    assert current_user is not None


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
        name='Uchpochmak',
        email='bashkort@example.com',
        password='eshkere!',
        password2='eshkere!',
        is_company=False,
    )

    new_user = await user_query.create(sa_session, user_schema=user)
    assert new_user is not None
    assert new_user.name == 'Uchpochmak'
    assert new_user.hashed_password != 'eshkere!'


@pytest.mark.asyncio
async def test_create_password_mismatch(sa_session):
    with pytest.raises(ValidationError):
        user = UserInSchema(
            name='Uchpochmak',
            email='bashkort@example.com',
            password='eshkere!',
            password2='eshkero',
            is_company=False,
        )
        await user_query.create(sa_session, user_schema=user)


@pytest.mark.asyncio
async def test_update(sa_session):
    user = UserFactory.build()
    sa_session.add(user)
    sa_session.flush()
    user.name = 'update_name'
    updated_user = await user_query.update(sa_session, user=user)
    res = await user_query.get_by_id(sa_session, user.id)
    assert updated_user.name == res.name
    assert updated_user.email == res.email
    assert updated_user.is_company == res.is_company
    assert res.name == 'update_name'
