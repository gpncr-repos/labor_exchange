import pytest

from core.security import hash_password
from fixtures.users import UserFactory


@pytest.mark.asyncio
async def test_log_norm(client_app, sa_session):
    passwd_user = "testtest"
    new_user = UserFactory.build(hashed_password=hash_password(passwd_user))
    sa_session.add(new_user)
    await sa_session.flush()
    response = await client_app.post(
        "/auth", json={"email": new_user.email, "password": passwd_user}
    )
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_log_miss_password(client_app, sa_session):
    passwd_user = "testtest"
    new_user = UserFactory.build(hashed_password=hash_password(passwd_user))
    sa_session.add(new_user)
    await sa_session.flush()
    response = await client_app.post(
        "/auth", json={"email": new_user.email, "password": passwd_user + "2"}
    )
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_log_miss_email(client_app, sa_session):
    passwd_user = "testtest"
    new_user = UserFactory.build(hashed_password=hash_password(passwd_user))
    sa_session.add(new_user)
    await sa_session.flush()
    response = await client_app.post(
        "/auth", json={"email": "2" + new_user.email, "password": passwd_user}
    )
    assert response.status_code == 401
