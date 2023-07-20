import pytest

from factories.jobs import JobFactory

URL_PREFIX = "/jobs"


@pytest.mark.asyncio
async def test_read(client_app):
    response = await client_app.get(URL_PREFIX)
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.parametrize(
    "current_user,expected_code",
    [("anonymous", 401), ("user", 403), ("company", 200)],
    indirect=["current_user"]
)
@pytest.mark.asyncio
async def test_create(client_app, expected_code):
    data = {
        "title": "job_title",
        "description": "job description",
        "salary_from": "200000.25",
        "salary_to": "300000.25",
        "is_active": True
    }
    response = await client_app.post(URL_PREFIX, json=data)
    assert response.status_code == expected_code


@pytest.mark.parametrize("salary_pair", [("50", "20"), ("100.676", "300.252")])
@pytest.mark.parametrize(
    "current_user",
    ["company"],
    indirect=["current_user"]
)
@pytest.mark.asyncio
async def test_create_incorrect_salary(client_app, salary_pair):
    data = {
        "title": "job_title",
        "description": "job description",
        "salary_from": salary_pair[0],
        "salary_to": salary_pair[1],
        "is_active": True
    }
    response = await client_app.post(URL_PREFIX, json=data)
    assert response.status_code == 422


@pytest.mark.parametrize(
    "current_user,expected_code",
    [("anonymous", 401), ("user", 403), ("company", 200)],
    indirect=["current_user"]
)
@pytest.mark.asyncio
async def test_update(client_app, sa_session, current_user, expected_code):
    job = JobFactory.build(user=current_user) if current_user else JobFactory.build()
    sa_session.add(job)
    await sa_session.flush()
    update_data = {
        "title": "updated_title",
        "description": "updated description",
        "salary_from": "120000",
        "salary_to": "140000",
        "is_active": not job.is_active
    }
    response = await client_app.put(f"{URL_PREFIX}/{job.id}", json=update_data)
    assert response.status_code == expected_code


@pytest.mark.parametrize(
    "current_user,expected_code",
    [("company", 404)],
    indirect=["current_user"]
)
@pytest.mark.asyncio
async def test_update_not_found(client_app, expected_code):
    update_data = {
        "title": "updated_title"
    }
    response = await client_app.put(f"{URL_PREFIX}/1", json=update_data)
    assert response.status_code == expected_code


@pytest.mark.parametrize(
    "current_user,expected_code",
    [("anonymous", 401), ("user", 403), ("company", 204)],
    indirect=["current_user"]
)
@pytest.mark.asyncio
async def test_delete(client_app, sa_session, current_user, expected_code):
    job = JobFactory.build(user=current_user) if current_user else JobFactory.build()
    sa_session.add(job)
    await sa_session.flush()
    response = await client_app.delete(f"{URL_PREFIX}/{job.id}")
    assert response.status_code == expected_code


@pytest.mark.parametrize(
    "current_user,expected_code",
    [("company", 404)],
    indirect=["current_user"]
)
@pytest.mark.asyncio
async def test_delete_not_found(client_app, current_user, expected_code):
    response = await client_app.delete(f"{URL_PREFIX}/1")
    assert response.status_code == expected_code


@pytest.mark.parametrize(
    "current_user,expected_code",
    [("anonymous", 401), ("user", 200), ("company", 403)],
    indirect=["current_user"]
)
@pytest.mark.asyncio
async def test_response(client_app, sa_session, expected_code):
    job = JobFactory.build()
    sa_session.add(job)
    await sa_session.flush()
    data = {
        "message": "Test response message"
    }
    response = await client_app.post(f"{URL_PREFIX}/{job.id}/response", json=data)
    assert response.status_code == expected_code


@pytest.mark.parametrize(
    "current_user,expected_code",
    [("user", 404)],
    indirect=["current_user"]
)
@pytest.mark.asyncio
async def test_response_not_found(client_app, expected_code):
    data = {
        "message": "Test response message"
    }
    response = await client_app.post(f"{URL_PREFIX}/1/response", json=data)
    assert response.status_code == expected_code


@pytest.mark.parametrize(
    "current_user,expected_code",
    [("anonymous", 401), ("user", 403), ("company", 200)],
    indirect=["current_user"]
)
@pytest.mark.asyncio
async def test_read_responses(client_app, sa_session, current_user, expected_code):
    job = JobFactory.build(user=current_user) if current_user else JobFactory.build()
    sa_session.add(job)
    await sa_session.flush()
    response = await client_app.get(f"{URL_PREFIX}/{job.id}/responses")
    assert response.status_code == expected_code


@pytest.mark.parametrize(
    "current_user,expected_code",
    [("company", 404)],
    indirect=["current_user"]
)
@pytest.mark.asyncio
async def test_read_responses_not_found(client_app, current_user, expected_code):
    response = await client_app.get(f"{URL_PREFIX}/1/responses")
    assert response.status_code == expected_code
