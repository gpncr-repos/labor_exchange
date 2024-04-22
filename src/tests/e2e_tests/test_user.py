import datetime
from random import randint

import pytest

from schemas import UserSchema

prefix = "/users"


@pytest.mark.asyncio
async def test_read_users(client_app):
    response_server = await client_app.get(prefix)
    assert response_server.status_code == 200
    assert len(response_server.json()) == 0


@pytest.mark.asyncio
async def test_create_user(client_app):
    new_user = {
        "name": "Vladislav",
        "email": "vladislav@gmail.com",
        "password": "vladvlad",
        "password2": "vladvlad",
        "is_company": bool(randint(0, 1)),
    }
    response_server = await client_app.post(prefix, json=new_user)
    response_user = UserSchema(**response_server.json())

    assert response_server.status_code == 200
    assert response_user.name == new_user["name"]
    assert response_user.email == new_user["email"]
    assert response_user.hashed_password
    assert response_user.is_company == new_user["is_company"]
    assert response_user.created_at
    assert (datetime.datetime.utcnow() - response_user.created_at).seconds < 60 * 2


@pytest.mark.asyncio
async def test_create_error(client_app):
    new_user = {
        "name": "Vladislav",
        "email": "vladislav@gmail.com",
        "password": "password",
        "password2": "ne_tot_password",
        "is_company": bool(randint(0, 1)),
    }

    response_server = await client_app.post(prefix, json=new_user)
    assert response_server.status_code == 422


@pytest.mark.asyncio
async def test_update_unauthorized_user(client_app):
    update_data_user = {"name": "Volodymyr", "email": "volody@gmail.com"}
    response_server = await client_app.put(f"{prefix}?id={0}", json=update_data_user)
    assert response_server.status_code == 403


@pytest.mark.parametrize("user", ["user", "company"], indirect=["user"])
@pytest.mark.asyncio
async def test_update_user(client_app, user: UserSchema):
    update_data_user = {
        "name": "Volodymyr",
        "email": "volody@gmail.com",
        "is_company": not user.is_company,
    }
    response_server = await client_app.put(
        f"{prefix}?id={user.id}", json=update_data_user
    )
    response_updated_user = UserSchema(**response_server.json())
    assert response_server.status_code == 200
    assert response_updated_user.name == "Volodymyr"
    assert response_updated_user.email == "volody@gmail.com"
    assert response_updated_user.is_company == update_data_user["is_company"]
    assert response_updated_user.hashed_password == user.hashed_password
    assert response_updated_user.created_at == user.created_at


@pytest.mark.parametrize("user", ["user", "company"], indirect=["user"])
@pytest.mark.asyncio
async def test_update_user_not_found(client_app, user: UserSchema):
    update_data_user = {
        "name": "Volodymyr",
    }
    response_server = await client_app.put(
        f"{prefix}?id={user.id + 1}", json=update_data_user
    )
    assert response_server.status_code == 404
