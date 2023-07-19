from datetime import datetime, timedelta

import pytest


@pytest.mark.asyncio
async def test_read(client_app):
    response = await client_app.get("/users")
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_create(client_app):
    data = {
        "name": "user",
        "email": "user@example.com",
        "password": "12345678",
        "password2": "12345678",
        "is_company": False
    }
    response = await client_app.post("/users", json=data)
    assert response.status_code == 200
    result = response.json()
    assert result["name"] == "user"
    assert result["email"] == "user@example.com"
    assert result["is_company"] is False
    assert isinstance(result["id"], int)
    assert abs(
        datetime.fromisoformat(result["created_at"]) - datetime.utcnow()
        ) < timedelta(minutes=1)


@pytest.mark.asyncio
async def test_create_pass_mismatch(client_app):
    data = {
        "name": "user",
        "email": "user@example.com",
        "password": "12345678",
        "password2": "1234567890",
        "is_company": False
    }
    response = await client_app.post("/users", json=data)
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_update_unauthorized(client_app):
    update_data = {
        "name": "updated_name",
    }
    response = await client_app.put("/users?id=1", json=update_data)
    assert response.status_code == 401


@pytest.mark.parametrize(
    "current_user",
    ["user"],
    indirect=["current_user"]
)
@pytest.mark.asyncio
async def test_update_not_found(client_app, current_user):
    update_data = {
        "name": "updated_name",
    }
    response = await client_app.put(f"/users?id={current_user.id + 1}", json=update_data)
    assert response.status_code == 404


@pytest.mark.parametrize(
    "current_user",
    ["user", "company"],
    indirect=["current_user"]
)
@pytest.mark.asyncio
async def test_update(client_app, current_user):
    update_data = {
        "name": "updated_name",
        "email": "newemail@example.com",
        "is_company": not current_user.is_company
    }
    response = await client_app.put(f"/users?id={current_user.id}", json=update_data)
    assert response.status_code == 200
    result = response.json()
    assert result["name"] == update_data["name"]
    assert result["email"] == update_data["email"]
    assert result["is_company"] == update_data["is_company"]
