import pytest


@pytest.mark.asyncio
async def test_read_main_empty(client_app):
    response = await client_app.get("/users")
    print(response.content)
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_read_main_with_one(client_app):
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
    # print(response.content)
    # response = client_app.get("/users/")
    assert response.status_code == 201
