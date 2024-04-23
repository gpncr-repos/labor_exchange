from unittest.mock import patch

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
    assert response_login_data["access_token"]["token"]
    assert response_login_data["access_token"]["token_type"]
    assert response_login_data["refresh_token"]["token"]
    assert response_login_data["refresh_token"]["token_type"]


@pytest.mark.asyncio
async def test_login_authorized_fail(client_app, sa_session):
    passwd_user = "testtest"
    new_user = UserFactory.build(hashed_password=hash_password(passwd_user))

    sa_session.add(new_user)
    await sa_session.flush()

    login_data = {"email": new_user.email, "password": "123456789"}

    response_server = await client_app.post(prefix, json=login_data)

    assert response_server.status_code == 401


@pytest.mark.asyncio
async def test_refresh_token(client_app, sa_session):
    passwd_user = "testtest"
    new_user = UserFactory.build(hashed_password=hash_password(passwd_user))
    sa_session.add(new_user)
    await sa_session.flush()
    login_data = {"email": new_user.email, "password": passwd_user}

    response_server = await client_app.post(prefix, json=login_data)
    response_login_data = response_server.json()
    data = {"Authorization": "Bearer " + response_login_data["refresh_token"]["token"]}
    response_server_refresh_token = await client_app.post(
        prefix + "/refresh", headers=data
    )
    refresh_update_token = response_server_refresh_token.json()

    assert response_server.status_code == 200
    assert response_server_refresh_token.status_code == 200
    assert refresh_update_token["token"]
    assert refresh_update_token["token_type"]


@pytest.mark.asyncio
async def test_refresh_token_expired(client_app, sa_session):
    with patch("core.security.REFRESH_TOKEN_EXPIRE_MINUTES", -1):
        passwd_user = "testtest"
        new_user = UserFactory.build(hashed_password=hash_password(passwd_user))
        sa_session.add(new_user)
        await sa_session.flush()
        login_data = {"email": new_user.email, "password": passwd_user}

        response_server = await client_app.post(prefix, json=login_data)
        response_login_data = response_server.json()
        data = {
            "Authorization": "Bearer " + response_login_data["refresh_token"]["token"]
        }
        response_server_refresh_token = await client_app.post(
            prefix + "/refresh", headers=data
        )
        assert response_server_refresh_token.status_code == 403


@pytest.mark.asyncio
async def test_access_token_expired(client_app, sa_session):
    with patch("core.security.ACCESS_TOKEN_EXPIRE_MINUTES", -1):
        passwd_user = "testtest"
        new_user = UserFactory.build(hashed_password=hash_password(passwd_user))
        sa_session.add(new_user)
        await sa_session.flush()
        login_data = {"email": new_user.email, "password": passwd_user}

        response_server = await client_app.post(prefix, json=login_data)
        response_login_data = response_server.json()
        data = {
            "Authorization": "Bearer " + response_login_data["access_token"]["token"]
        }
        response_server = await client_app.put("/users", headers=data)
        assert response_server.status_code == 403


@pytest.mark.asyncio
async def test_refresh_token_access(client_app, sa_session):
    passwd_user = "testtest"
    new_user = UserFactory.build(
        hashed_password=hash_password(passwd_user), is_company=True
    )
    sa_session.add(new_user)
    await sa_session.flush()
    login_data = {"email": new_user.email, "password": passwd_user}

    response_server = await client_app.post(prefix, json=login_data)
    response_login_data = response_server.json()
    data = {"Authorization": "Bearer " + response_login_data["refresh_token"]["token"]}

    response_server = await client_app.put("/users", headers=data)

    assert response_server.status_code == 403
    assert response_server.json()["detail"] == "Invalid or inappropriate auth token"
