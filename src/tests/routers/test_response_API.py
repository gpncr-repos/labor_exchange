import json

import pytest

from fixtures.jobs import JobFactory
from fixtures.responses import ResponseCreateFactory, ResponseFactory
from fixtures.users import UserFactory


@pytest.mark.asyncio
async def test_read_response_by_id(client_app, current_user, sa_session):
    current_user.is_company = True
    sa_session.add(current_user)
    sa_session.flush()
    job = JobFactory.build()
    job.user_id = current_user.id
    sa_session.add(job)
    sa_session.flush()
    count_workers = 10
    list_of_workers = []
    for _ in range(count_workers):
        user = UserFactory.build()
        user.is_company = False
        sa_session.add(user)
        sa_session.flush()
        response = ResponseFactory.build()
        response.job_id = job.id
        response.user_id = user.id
        sa_session.add(response)
        sa_session.flush()
        list_of_workers.append(user)
    response = await client_app.get(f"/responses/responses_job_id/{job.id}")
    assert response.status_code == 200
    assert len(json.loads((response.content).decode("utf-8").replace("'", '"'))) == count_workers
    response = await client_app.get("/responses/responses_job_id/-1")
    assert response.status_code == 204


# вопрос про аутентификацию случайных пользователей


@pytest.mark.asyncio
async def test_read_all_user_responses(client_app, current_user, sa_session):
    emploer = UserFactory.build()
    emploer.is_company = True
    sa_session.add(emploer)
    sa_session.flush()

    current_user.is_company = False
    sa_session.add(current_user)
    sa_session.flush()

    count_responses = 10
    for _ in range(count_responses):
        job = JobFactory.build()
        job.user_id = emploer.id
        sa_session.add(job)
        sa_session.flush()

        response = ResponseFactory.build()
        response.job_id = job.id
        response.user_id = current_user.id
        sa_session.add(response)
        sa_session.flush()

    response = await client_app.get("/responses/responses_user")
    assert response.status_code == 200
    assert len(json.loads((response.content).decode("utf-8").replace("'", '"'))) == count_responses


@pytest.mark.asyncio
async def test_read_all_user_company_responses(client_app, current_user, sa_session):
    emploer = UserFactory.build()
    emploer.is_company = True
    sa_session.add(emploer)
    sa_session.flush()

    current_user.is_company = False
    sa_session.add(current_user)
    sa_session.flush()

    count_responses = 10
    for _ in range(count_responses):
        job = JobFactory.build()
        job.user_id = emploer.id
        sa_session.add(job)
        sa_session.flush()

        response = ResponseFactory.build()
        response.job_id = job.id
        response.user_id = current_user.id
        sa_session.add(response)
        sa_session.flush()

    current_user.is_company = True
    sa_session.add(current_user)
    sa_session.flush()

    response = await client_app.get("/responses/responses_user")
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_read_all_user_responses_empty(client_app, current_user, sa_session):
    current_user.is_company = False
    sa_session.add(current_user)
    sa_session.flush()

    response = await client_app.get("/responses/responses_user")
    assert response.status_code == 204


@pytest.mark.asyncio
async def test_post_response_company(client_app, current_user, sa_session):
    emploer = UserFactory.build()
    emploer.is_company = True
    sa_session.add(emploer)
    sa_session.flush()

    job = JobFactory.build()
    job.user_id = emploer.id
    sa_session.add(job)
    sa_session.flush()

    current_user.is_company = False
    sa_session.add(current_user)
    sa_session.flush()

    response_massage = (ResponseCreateFactory.stub()).__dict__
    response = await client_app.post(f"/responses/post_response/{job.id}", json=response_massage)
    assert response.status_code == 201
