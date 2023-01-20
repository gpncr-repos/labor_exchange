import pytest
from fixtures.users import UserFactory
from fixtures.jobs import JobFactory
from fixtures.responses import ResponseFactory

import schemas

# todo(vvnumb): могут быть проблемы, если использовать не пустую тестовую БД

# todo(vvnumb): можно написать фикстуры для получения пользователя


def fake_commit(session, inst):
    session.add(inst)
    session.flush()


@pytest.mark.asyncio
async def test_api_get_jobs(sa_session, client_app):
    user = UserFactory.build()
    fake_commit(sa_session, user)

    number_of_jobs = 10
    jobs = []
    for _ in range(number_of_jobs):
        job = JobFactory.build()
        job.user_id = user.id
        jobs.append(job)

        sa_session.add(job)

    sa_session.flush()

    http_response_jobs = await client_app.get("/jobs/list")

    http_response_jobs = http_response_jobs.json()

    assert len(http_response_jobs) == number_of_jobs


@pytest.mark.asyncio
async def test_api_get_job(sa_session, client_app):
    user = UserFactory.build()
    fake_commit(sa_session, user)

    job = JobFactory.build()
    job.user_id = user.id

    fake_commit(sa_session, job)

    http_request_job = await client_app.get(f"/jobs/{job.id}")
    assert http_request_job.status_code == 200
    http_request_job = http_request_job.json()

    assert http_request_job["id"] == job.id


@pytest.mark.asyncio
async def test_api_get_unexisting_job(sa_session, client_app):
    user = UserFactory.build()
    fake_commit(sa_session, user)

    job = JobFactory.build()
    job.user_id = user.id

    fake_commit(sa_session, job)

    http_request_job = await client_app.get(f"/jobs/{job.id + 1}")
    assert http_request_job.status_code == 404


@pytest.mark.asyncio
async def test_api_create_job(sa_session, client_app, current_user):
    current_user.is_company = True
    fake_commit(sa_session, current_user)

    fake_job = JobFactory.build()
    job_payload = schemas.JobInSchema(
        title=fake_job.title,
        description=fake_job.description,
        salary_from=fake_job.salary_from,
        salary_to=fake_job.salary_to,
    )

    http_response_job = await client_app.post("/jobs/", json=job_payload.dict())
    assert http_response_job.status_code == 200
    assert http_response_job.json()["title"] == fake_job.title


@pytest.mark.asyncio
async def test_api_user_create_job(sa_session, client_app, current_user):
    current_user.is_company = False
    fake_commit(sa_session, current_user)

    fake_job = JobFactory.build()
    job_payload = schemas.JobInSchema(
        title=fake_job.title,
        description=fake_job.description,
        salary_from=fake_job.salary_from,
        salary_to=fake_job.salary_to,
    )

    http_response_job = await client_app.post("/jobs/", json=job_payload.dict())
    assert http_response_job.status_code == 405


@pytest.mark.asyncio
async def test_update_job(sa_session, client_app, current_user, job_repo):
    current_user.is_company = True
    fake_commit(sa_session, current_user)

    fake_job = JobFactory.build()
    job = await job_repo.create(sa_session, fake_job)
    job_payload = schemas.JobInSchema(
        title=fake_job.title + "1"
    )

    http_response_job = await client_app.patch(f"/jobs/{job.id}", json=job_payload.dict())
    assert http_response_job.status_code == 200
    assert http_response_job.json()["title"] == job_payload.title


@pytest.mark.asyncio
async def test_user_try_update_job(sa_session, client_app, current_user, job_repo):
    current_user.is_company = False
    fake_commit(sa_session, current_user)

    fake_job = JobFactory.build()
    job = await job_repo.create(sa_session, fake_job)
    job_payload = schemas.JobInSchema(
        title=fake_job.title + "1"
    )

    http_response_job = await client_app.patch(f"/jobs/{job.id}", json=job_payload.dict())
    assert http_response_job.status_code == 405


@pytest.mark.asyncio
async def test_delete_job(sa_session, client_app, current_user, job_repo):
    current_user.is_company = True
    fake_commit(sa_session, current_user)

    fake_job = JobFactory.build()
    job = await job_repo.create(sa_session, fake_job)

    http_response_job = await client_app.delete(f"/jobs/{job.id}")
    assert http_response_job.status_code == 200


@pytest.mark.asyncio
async def test_user_delete_job(sa_session, client_app, current_user, job_repo):
    current_user.is_company = False
    fake_commit(sa_session, current_user)

    fake_job = JobFactory.build()
    job = await job_repo.create(sa_session, fake_job)

    http_response_job = await client_app.delete(f"/jobs/{job.id}")
    assert http_response_job.status_code == 405


@pytest.mark.asyncio
async def test_get_response(sa_session, client_app, current_user, response_repo):
    current_user.is_company = True
    fake_commit(sa_session, current_user)

    fake_response = ResponseFactory.build()
    job_id = fake_response.job_id
    await response_repo.create(sa_session, fake_response)

    http_response_job = await client_app.get(f"/jobs/responses/{job_id}")
    assert http_response_job.status_code == 200
    assert len(http_response_job.json()) == 1


@pytest.mark.asyncio
async def test_user_get_response(sa_session, client_app, current_user, response_repo):
    current_user.is_company = False
    fake_commit(sa_session, current_user)

    fake_response = ResponseFactory.build()
    job_id = fake_response.job_id
    await response_repo.create(sa_session, fake_response)

    http_response_job = await client_app.get(f"/jobs/responses/{job_id}")
    assert http_response_job.status_code == 405


@pytest.mark.asyncio
async def test_make_response(sa_session, client_app, current_user, job_repo):
    current_user.is_company = False
    fake_commit(sa_session, current_user)

    fake_response = ResponseFactory.build()

    job = fake_response.job
    await job_repo.create(sa_session, job)

    http_response_job = await client_app.post(f"/jobs/respond/{job.id}", json=dict(comment="test"))
    assert http_response_job.status_code == 200


@pytest.mark.asyncio
async def test_employer_make_response(sa_session, client_app, current_user, job_repo):
    current_user.is_company = True
    fake_commit(sa_session, current_user)

    fake_response = ResponseFactory.build()

    job = fake_response.job
    await job_repo.create(sa_session, job)

    http_response_job = await client_app.post(f"/jobs/respond/{job.id}", json=dict(comment="test"))
    assert http_response_job.status_code == 405
