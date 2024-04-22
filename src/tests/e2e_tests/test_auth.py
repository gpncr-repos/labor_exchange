import pytest

from core.security import hash_password
from fixtures.users import UserFactory

prefix = "/auth"


@pytest.mark.asyncio
async def test_login_authorized(client_app, sa_session):
    passwd_user = "testtest"
    new_user = UserFactory.build(hashed_password=hash_password(passwd_user))

    sa_session.add(new_user)
    await sa_session.flush()

    login_data = {"email": new_user.email, "password": passwd_user}

    response_server = await client_app.post(prefix, json=login_data)
    response_login_data = response_server.json()

    assert response_server.status_code == 200
    assert response_login_data["access_token"]
    assert response_login_data["token_type"]


@pytest.mark.asyncio
async def test_login_authorized_fail(client_app, sa_session):
    passwd_user = "testtest"
    new_user = UserFactory.build(hashed_password=hash_password(passwd_user))

    sa_session.add(new_user)
    await sa_session.flush()

    login_data = {"email": new_user.email, "password": "123456789"}

    response_server = await client_app.post(prefix, json=login_data)

    assert response_server.status_code == 401
