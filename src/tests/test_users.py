from datetime import datetime

import pytest
from applications.queries import user_queries as user_query
from core.security import hash_password
from domain.dm_schemas import DMUser
from infrastructure.repos import RepoUser
from tests.fixtures.factories import UserFactory
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
    assert all((
        all_users[0].name == user.name,
        all_users[0].email == user.email,
        all_users[0].created_at == user.created_at,
        all_users[0].is_company == user.is_company,
    )), "Добавленный пользователь не оказался первым в выборке из базы"


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
    new_user = await repo_user.add(user)

    current_user = await repo_user.get_by_id(new_user.id)
    assert current_user is not None, "Ошибки при получении по идентификатору записи о пользователе из базы"
    assert current_user.id == new_user.id


@pytest.mark.asyncio
async def test_get_by_email(sa_session):
    user = UserFactory.build()
    repo_user = RepoUser(sa_session)
    new_user = await repo_user.add(user)

    current_user = await repo_user.get_by_email(user.email)
    assert current_user is not None
    assert current_user.id == new_user.id


@pytest.mark.asyncio
async def test_create(sa_session):
    # user = UserInSchema(
    user = DMUser(
        name="Uchpochmak",
        email="bashkort@example.com",
        hashed_password=hash_password("eshkere!"),
        is_company=False,
        created_at=datetime.utcnow(),
    )

    repo_user = RepoUser(sa_session)
    new_user = await repo_user.add(obj_to_add=user)
    assert new_user is not None
    assert new_user.name == "Uchpochmak"
    assert new_user.hashed_password != "eshkere!"

# Несовпаденеи паролей не проверяется репозиторием
# @pytest.mark.asyncio
# async def test_create_password_mismatch(sa_session):
#     with pytest.raises(ValidationError):
#         # user = UserInSchema(
#         #     name="Uchpochmak",
#         #     email="bashkort@example.com",
#         #     password="eshkere!",
#         #     password2="eshkero!",
#         #     is_company=False
#         # )
#         user = DMUser(
#             name="Uchpochmak",
#             email="bashkort@example.com",
#             password=hash_password("eshkero!"),
#             is_company=False,
#             created_at=datetime.utcnow(),
#         )
#         repo_user = RepoUser(sa_session)
#         await repo_user.add(obj_to_add=user)
#     print("hello world")


@pytest.mark.asyncio
async def test_update(sa_session):
    user = UserFactory.build()
    repo_user = RepoUser(sa_session)
    new_user = await repo_user.add(user)

    new_user.name = "updated_name"
    upd_user = await repo_user.update(user=new_user)
    assert new_user.id == upd_user.id
    assert upd_user.name == "updated_name"
