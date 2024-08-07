import pytest


@pytest.mark.asyncio
async def test_read_all_delete(client_app):
    response = await client_app.get("/users")
    assert response.status_code == 200
    response = await client_app.delete("/users/delete")
    response = await client_app.get("/users")
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_read_users_by_id(client_app, current_user):
    response = await client_app.get(f"/users/{current_user.id}")
    assert response.status_code == 200
    response = await client_app.get("/users/2")
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_post_user(client_app):
    response = await client_app.post(
        "/users/post",
        json={
            "name": "string",
            "email": "user@example.com",
            "password": "stringst",
            "password2": "stringst",
            "is_company": False,
        },
    )
    assert response.status_code == 201


@pytest.mark.asyncio
async def test_put_user(client_app, current_user):
    response = await client_app.put(
        "/users/put",
        json={
            "name": current_user.name + "_update",
        },
    )
    assert response.status_code == 200
