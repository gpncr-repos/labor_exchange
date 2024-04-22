from typing import List

import pytest

from fixtures.jobs import JobFactory
from schemas import UserSchema

prefix = "/jobs"


@pytest.mark.asyncio
async def test_read_jobs(client_app):
    response_server = await client_app.get(prefix)
    assert response_server.status_code == 200
    assert len(response_server.json()) == 0


@pytest.mark.asyncio
async def test_bad_request(client_app):
    for param in ("limit", "skip"):
        response_server = await client_app.get(f"{prefix}?{param}=-1")
        assert response_server.status_code == 400


@pytest.mark.parametrize("user", ["user", "company"], indirect=["user"])
@pytest.mark.asyncio
async def test_get_job_by_id(client_app, sa_session, user: UserSchema):
    new_job = JobFactory.build(user=user)
    sa_session.add(new_job)
    await sa_session.flush()

    response_server = await client_app.get(f"{prefix}/{new_job.id}")

    assert response_server.status_code == 200


@pytest.mark.asyncio
async def test_not_found_by_id(client_app):
    response_server = await client_app.get(f"{prefix}/{0}")
    assert response_server.status_code == 404


@pytest.mark.parametrize(
    "user,code",
    [("unauthorized", 403), ("user", 401), ("company", 200)],
    indirect=["user"],
)
@pytest.mark.asyncio
async def test_create_job(client_app, sa_session, user: UserSchema, code: int):
    new_job = {
        "title": "Python dev",
        "description": "fullstack developer",
        "salary_from": 250_000,
        "salary_to": 300_000,
    }

    response_server = await client_app.post(prefix, json=new_job)

    assert response_server.status_code == code
    if response_server.status_code == 200:
        assert response_server.json()["is_active"]


@pytest.mark.parametrize(
    "user,code",
    [("unauthorized", 403), ("user", 401), ("company", 200)],
    indirect=["user"],
)
@pytest.mark.asyncio
async def test_update_job_access(client_app, sa_session, user: UserSchema, code: int):
    new_job = JobFactory.build(user=user) if user else JobFactory.build()
    sa_session.add(new_job)
    await sa_session.flush()

    update_data = {
        "title": "PythonDev",
        "description": "fullstack developer",
        "salary_from": 250_000,
        "salary_to": 300_000,
        "is_active": not new_job.is_active,
    }

    response_server = await client_app.put(f"{prefix}/{new_job.id}", json=update_data)

    assert response_server.status_code == code


@pytest.mark.parametrize("user", ["company"], indirect=["user"])
@pytest.mark.asyncio
async def test_update_job(client_app, sa_session, user: UserSchema):
    new_job = JobFactory.build(user=user)
    sa_session.add(new_job)
    await sa_session.flush()

    update_data = {
        "title": "PythonDev",
        "description": "fullstack developer",
        "salary_from": 250_000,
        "salary_to": 300_000,
        "is_active": not new_job.is_active,
    }

    response_server = await client_app.put(f"{prefix}/{new_job.id}", json=update_data)
    response_updated_data = response_server.json()

    assert response_server.status_code == 200
    assert update_data["title"] == response_updated_data["title"]
    assert update_data["description"] == response_updated_data["description"]
    assert update_data["salary_from"] == response_updated_data["salary_from"]
    assert update_data["salary_to"] == response_updated_data["salary_to"]
    assert update_data["is_active"] == response_updated_data["is_active"]
    assert isinstance(response_updated_data["salary_from"], float)
    assert isinstance(response_updated_data["salary_to"], float)


@pytest.mark.parametrize(
    "salary, code", [((100, 1000), 200), ((1000, 1), 422), ((1000, None), 200)]
)
@pytest.mark.parametrize("user", ["company"], indirect=["user"])
@pytest.mark.asyncio
async def test_update_job_check_salary_valid(
    client_app, sa_session, user: UserSchema, salary: List[float], code: int
):
    new_job = JobFactory.build(user=user)
    sa_session.add(new_job)
    await sa_session.flush()

    update_data = {
        "title": "PythonDev",
        "description": "fullstack developer",
        "salary_from": salary[0],
        "salary_to": salary[1],
        "is_active": not new_job.is_active,
    }

    response_server = await client_app.put(f"{prefix}/{new_job.id}", json=update_data)

    assert response_server.status_code == code


@pytest.mark.parametrize(
    "user,code",
    [("unauthorized", 403), ("user", 401), ("company", 200)],
    indirect=["user"],
)
@pytest.mark.asyncio
async def test_delete_job_by_id_access(
    client_app, sa_session, user: UserSchema, code: int
):
    new_job = JobFactory.build(user=user) if user else JobFactory.build()
    sa_session.add(new_job)
    await sa_session.flush()

    response_server = await client_app.delete(f"{prefix}/{new_job.id}")

    assert response_server.status_code == code


@pytest.mark.parametrize("user", ["company"], indirect=["user"])
@pytest.mark.asyncio
async def test_delete_job_by_id(client_app, sa_session, user: UserSchema):
    new_job = JobFactory.build(user=user)
    sa_session.add(new_job)
    await sa_session.flush()

    response_server = await client_app.delete(f"{prefix}/{new_job.id}")
    response_get_job = await client_app.get(f"{prefix}/{new_job.id}")

    assert response_server.status_code == 200
    assert response_get_job.status_code == 404
