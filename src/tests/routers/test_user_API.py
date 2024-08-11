import json

import pytest

from fixtures.users import UserCreateFactory


@pytest.mark.asyncio
async def test_read_current_user_and_delete(client_app):
    response = await client_app.get("/users")
    assert response.status_code == 200

    response = await client_app.delete("/users")
    response = await client_app.get("/users")
    assert response.status_code == 204


@pytest.mark.asyncio
async def test_read_limit_and_skip(client_app):
    response = await client_app.delete("/users")
    count_user = 10
    for _ in range(count_user):
        user = (UserCreateFactory.stub()).__dict__
        user["password2"] = user["password"]
        response = await client_app.post("/users", json=user)
    limit = 8
    skip = 5
    response = await client_app.get(f"/users?limit={limit}&skip={skip}")
    assert len(json.loads((response.content).decode("utf-8").replace("'", '"'))) == min(
        count_user - skip, limit
    )


@pytest.mark.asyncio
async def test_read_users_by_id(client_app, current_user):
    response = await client_app.get(f"/users/{current_user.id}")
    assert response.status_code == 200
    response = await client_app.get("/users/2")
    assert response.status_code == 204


@pytest.mark.asyncio
async def test_post_user(client_app):
    user = (UserCreateFactory.stub()).__dict__
    user["password2"] = user["password"]
    response = await client_app.post("/users", json=user)
    assert response.status_code == 201


@pytest.mark.asyncio
async def test_put_user(client_app, current_user):
    response = await client_app.put(
        "/users",
        json={
            "name": current_user.name + "_update",
        },
    )
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_delete_current(client_app):
    response = await client_app.delete("/users")
    response = await client_app.get("/users")
    assert response.status_code == 204
