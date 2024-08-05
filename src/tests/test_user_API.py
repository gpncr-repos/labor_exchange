from schemas import UserCreateSchema


def test_read_main_empty(client_app):
    response = client_app.get("/users")
    assert response.status_code == 422


def test_read_main_with_one(client_app):
    response = client_app.post(
        "/users/post",
        json={
            "name": "string",
            "email": "user@example.com",
            "password": "stringst",
            "password2": "stringst",
            "is_company": False,
        },
    )
    print(response.content)
    # response = client_app.get("/users/")
    assert response.status_code == 201
