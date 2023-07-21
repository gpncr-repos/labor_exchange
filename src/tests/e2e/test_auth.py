import pytest

from factories.users import UserFactory
from core.security import hash_password

URL_PREFIX = "/auth"


@pytest.mark.asyncio
async def test_login(client_app, sa_session):
    password = "very_secure_password"
    user = UserFactory.build(hashed_password=hash_password(password))
    sa_session.add(user)
    await sa_session.flush()
    data = {"username": user.email, "password": password}
    response = await client_app.post(URL_PREFIX, data=data)

    assert response.status_code == 200
    result = response.json()
    assert result["access_token"]
    assert result["refresh_token"]
    assert result["token_type"] == "Bearer"


@pytest.mark.asyncio
async def test_refresh_token(client_app, sa_session):
    password = "very_secure_password"
    user = UserFactory.build(hashed_password=hash_password(password))
    sa_session.add(user)
    await sa_session.flush()
    data = {"username": user.email, "password": password}
    response = await client_app.post(URL_PREFIX, data=data)

    refresh_token = response.json()["refresh_token"]
    data = {"refresh_token": refresh_token}
    response = await client_app.post(f"{URL_PREFIX}/refresh-token", json=data)

    assert response.status_code == 200
    result = response.json()
    assert result["access_token"]
    assert result["refresh_token"]
    assert result["token_type"] == "Bearer"


@pytest.mark.asyncio
async def test_refresh_with_access_token(client_app, sa_session):
    password = "very_secure_password"
    user = UserFactory.build(hashed_password=hash_password(password))
    sa_session.add(user)
    await sa_session.flush()
    data = {"username": user.email, "password": password}
    response = await client_app.post(URL_PREFIX, data=data)

    refresh_token = response.json()["access_token"]
    data = {"refresh_token": refresh_token}
    response = await client_app.post(f"{URL_PREFIX}/refresh-token", json=data)

    assert response.status_code == 403
    assert response.json()["detail"] == "Invalid refresh token!"


@pytest.mark.asyncio
async def test_refresh_with_expired_token(client_app, sa_session, mocker):
    mocker.patch("core.security.REFRESH_TOKEN_EXPIRE_MINUTES", -180)
    password = "very_secure_password"
    user = UserFactory.build(hashed_password=hash_password(password))
    sa_session.add(user)
    await sa_session.flush()
    data = {"username": user.email, "password": password}
    response = await client_app.post(URL_PREFIX, data=data)

    refresh_token = response.json()["refresh_token"]
    data = {"refresh_token": refresh_token}
    response = await client_app.post(f"{URL_PREFIX}/refresh-token", json=data)

    assert response.status_code == 403
    assert response.json()["detail"] == "Invalid refresh token!"


@pytest.mark.asyncio
async def test_access_with_refresh_token(client_app, sa_session):
    password = "very_secure_password"
    user = UserFactory.build(hashed_password=hash_password(password))
    sa_session.add(user)
    await sa_session.flush()
    data = {"username": user.email, "password": password}
    response = await client_app.post(URL_PREFIX, data=data)

    access_token = response.json()["refresh_token"]
    headers = {"Authorization": f"Bearer {access_token}"}
    response = await client_app.put("/users", headers=headers)

    assert response.status_code == 403
    assert response.json()["detail"] == "Credentials are not valid!"


@pytest.mark.asyncio
async def test_access_with_expired_token(client_app, sa_session, mocker):
    mocker.patch("core.security.ACCESS_TOKEN_EXPIRE_MINUTES", -60)
    password = "very_secure_password"
    user = UserFactory.build(hashed_password=hash_password(password))
    sa_session.add(user)
    await sa_session.flush()
    data = {"username": user.email, "password": password}
    response = await client_app.post(URL_PREFIX, data=data)

    access_token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}
    response = await client_app.put("/users", headers=headers)

    assert response.status_code == 403
    assert response.json()["detail"] == "Credentials are not valid!"
