import pytest

from fixtures.jobs import JobFactory
from fixtures.responses import ResponseFactory
from schemas import UserSchema

prefix = "/responses"


@pytest.mark.parametrize(
    "user, code",
    [("unauthorized", 403), ("user", 401), ("company", 200)],
    indirect=["user"],
)
@pytest.mark.asyncio
async def test_read_responses_access(
    client_app, sa_session, user: UserSchema, code: int
):
    new_job = JobFactory.build(user=user) if user else JobFactory.build()
    new_response = (
        ResponseFactory.build(user=user, job=new_job)
        if user
        else ResponseFactory.build(job=new_job)
    )
    sa_session.add_all((new_job, new_response))
    await sa_session.flush()

    response_server = await client_app.get(f"{prefix}/{new_job.id}")

    assert response_server.status_code == code


@pytest.mark.parametrize("user", ["company"], indirect=["user"])
@pytest.mark.asyncio
async def test_read_responses_not_found(client_app, sa_session, user: UserSchema):
    new_job = JobFactory.build(user=user)
    new_response = ResponseFactory.build(user=user, job=new_job)
    sa_session.add_all((new_job, new_response))
    await sa_session.flush()

    response_server = await client_app.get(f"{prefix}/{new_job.id + 1}")

    assert response_server.status_code == 404


@pytest.mark.parametrize("user", ["company"], indirect=["user"])
@pytest.mark.asyncio
async def test_read_responses(client_app, sa_session, user: UserSchema):
    new_job = JobFactory.build(user=user)
    new_response = ResponseFactory.build(user=user, job=new_job)
    sa_session.add_all((new_job, new_response))
    await sa_session.flush()

    response_server = await client_app.get(f"{prefix}/{new_job.id}")
    response_data = response_server.json()

    assert response_server.status_code == 200
    assert len(response_data) == 1
    assert new_response.message == response_data[0]["message"]
    assert new_response.user_id == response_data[0]["user_id"]


@pytest.mark.parametrize(
    "user, code",
    [("unauthorized", 403), ("user", 200), ("company", 401)],
    indirect=["user"],
)
@pytest.mark.asyncio
async def test_create_response(client_app, sa_session, user: UserSchema, code: int):
    new_job = JobFactory.build()
    sa_session.add(new_job)
    await sa_session.flush()

    response_data = {"message": "Test create response"}

    response_server = await client_app.post(
        f"{prefix}/{new_job.id}", data=response_data
    )

    assert response_server.status_code == code


@pytest.mark.parametrize("user", ["user"], indirect=["user"])
@pytest.mark.asyncio
async def test_create_response_not_found(client_app, sa_session, user: UserSchema):
    new_job = JobFactory.build()
    sa_session.add(new_job)
    await sa_session.flush()

    response_data = {"message": "Test create response"}

    response_server = await client_app.post(
        f"{prefix}/{new_job.id + 1}", data=response_data
    )

    assert response_server.status_code == 404
