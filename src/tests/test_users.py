import pytest
from applications.queries import user_queries as user_query
from infrastructure.repos import RepoUser
from tests.fixtures.users import UserFactory
from api.schemas.user import UserInSchema
from pydantic import ValidationError


@pytest.mark.asyncio
async def test_get_all(sa_session):
    # user = UserFactory.build()
    # sa_session.add(user)
    # sa_session.flush()
    #
    # get_req = await user_query.get_all(sa_session)
    # assert not get_req.errors, "Ошибка при получении списка пользователей"
    # all_users = get_req.result
    # assert all_users, "Не удалось получить список пользователей из базы"
    # assert len(all_users) == 1, "Кол-во пользователей в базе отличается от кол-ва добавленных пользователей"
    # assert all_users[0] == user, "Добавленный пользователь не оказался первым в выборке из базы"
    user = UserFactory.build()
    repo_user = RepoUser(sa_session)
    await repo_user.add(user)

    all_users = await repo_user.get_all()
    assert all_users, "Не удалось получить список пользователей из базы"
    assert len(all_users) == 1, "Кол-во пользователей в базе отличается от кол-ва добавленных пользователей"
    assert all_users[0] == user, "Добавленный пользователь не оказался первым в выборке из базы"



@pytest.mark.asyncio
async def test_get_by_id(sa_session):

    # user = UserFactory.build()
    # sa_session.add(user)
    # sa_session.flush()
    #
    # get_req = await user_query.get_by_id(sa_session, user.id)
    # assert not get_req.errors, "Ошибки при получении по идентификатору записи о пользователе из базы"
    # current_user = get_req.result
    # assert current_user is not None
    # assert current_user.id == user.id
    user = UserFactory.build()
    repo_user = RepoUser(sa_session)
    await repo_user.add(user)

    current_user = await repo_user.get_by_id(user.id)
    assert current_user is not None, "Ошибки при получении по идентификатору записи о пользователе из базы"
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

    add_req = await user_query.create(sa_session, user_schema=user)
    assert not add_req.errors, "Ошибки при создании пользователя"
    new_user = add_req.result
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
    print("hello world")


@pytest.mark.asyncio
async def test_update(sa_session):
    user = UserFactory.build()
    sa_session.add(user)
    sa_session.flush()

    user.name = "updated_name"
    upd_req = await user_query.update(sa_session, user=user)
    assert not upd_req.errors, "Ошибки при редактировании параметров пользователя"
    updated_user = upd_req.result
    assert user.id == updated_user.id
    assert updated_user.name == "updated_name"
