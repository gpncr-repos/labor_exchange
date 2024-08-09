import json

import pytest

from fixtures.jobs import JobCreateFactory, JobFactory
from fixtures.users import UserFactory


@pytest.mark.asyncio
async def test_read_job_by_id(client_app, current_user, sa_session):
    count_jobs = 10
    list_of_jobs_id = []
    for _ in range(count_jobs):
        job = JobFactory.build()
        job.user_id = current_user.id
        sa_session.add(job)
        list_of_jobs_id.append(job.id)

    for job_id in list_of_jobs_id:
        response = await client_app.get(f"/jobs/{job_id}")
        assert response.status_code == 200

    response = await client_app.get("/jobs/-1")
    assert response.status_code == 204


@pytest.mark.asyncio
async def test_read_jobs_limit_and_skip(client_app, current_user, sa_session):
    count_jobs = 10
    for _ in range(count_jobs):
        job = JobFactory.build()
        job.user_id = current_user.id
        sa_session.add(job)
    limit = 8
    skip = 5
    response = await client_app.get(f"/jobs?limit={limit}&skip={skip}")
    assert response.status_code == 200
    assert len(json.loads((response.content).decode("utf-8").replace("'", '"'))) == min(
        count_jobs - skip, limit
    )


@pytest.mark.asyncio
async def test_post_jobs_company(client_app, current_user, sa_session):
    current_user.is_company = True
    sa_session.add(current_user)
    sa_session.flush()
    job = (JobCreateFactory.stub()).__dict__
    response = await client_app.post("/jobs/post_job", json=job)
    assert response.status_code == 201


@pytest.mark.asyncio
async def test_post_jobs_not_company(client_app, current_user, sa_session):
    current_user.is_company = False
    sa_session.add(current_user)
    sa_session.flush()
    job = (JobCreateFactory.stub()).__dict__
    response = await client_app.post("/jobs/post_job", json=job)
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_put_job_real(client_app, current_user, sa_session):
    job = JobFactory.build()
    job.user_id = current_user.id
    sa_session.add(job)

    current_user.is_company = True
    sa_session.add(current_user)
    sa_session.flush()
    response = await client_app.patch(
        f"/jobs/patch_job/{job.id}",
        json={"title": job.title + "_update"},
    )
    print(response.content)
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_put_job_not_company(client_app, current_user, sa_session):
    job = JobFactory.build()
    job.user_id = current_user.id
    sa_session.add(job)

    current_user.is_company = False
    sa_session.add(current_user)
    sa_session.flush()
    response = await client_app.patch(
        f"/jobs/patch_job/{job.id}",
        json={"title": job.title + "_update"},
    )
    print(response.content)
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_put_job_dont_find(client_app, current_user, sa_session):
    job = JobFactory.build()
    job.user_id = current_user.id
    sa_session.add(job)

    current_user.is_company = True
    sa_session.add(current_user)
    sa_session.flush()
    response = await client_app.patch(
        f"/jobs/patch_job/{job.id+1}",
        json={"title": job.title + "_update"},
    )
    print(response.content)
    assert response.status_code == 204


@pytest.mark.asyncio
async def test_put_job_not_user(client_app, current_user, sa_session):
    current_user.is_company = True
    sa_session.add(current_user)

    user = UserFactory.build()
    user.is_company = True
    sa_session.add(user)
    sa_session.flush()

    job = JobFactory.build()
    job.user_id = user.id
    sa_session.add(job)
    sa_session.flush()

    response = await client_app.patch(
        f"/jobs/patch_job/{job.id}",
        json={"title": job.title + "_update"},
    )
    print(response.content)
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_delete_job_real(client_app, current_user, sa_session):
    job = JobFactory.build()
    job.user_id = current_user.id
    sa_session.add(job)

    current_user.is_company = True
    sa_session.add(current_user)
    sa_session.flush()
    response = await client_app.delete(f"/jobs/delete/{job.id}")
    print(response.content)
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_delete_job_not_company(client_app, current_user, sa_session):
    job = JobFactory.build()
    job.user_id = current_user.id
    sa_session.add(job)

    current_user.is_company = False
    sa_session.add(current_user)
    sa_session.flush()
    response = await client_app.delete(f"/jobs/delete/{job.id}")
    print(response.content)
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_delete_job_dont_find(client_app, current_user, sa_session):
    job = JobFactory.build()
    job.user_id = current_user.id
    sa_session.add(job)

    current_user.is_company = True
    sa_session.add(current_user)
    sa_session.flush()
    response = await client_app.delete(f"/jobs/delete/{job.id+1}")
    print(response.content)
    assert response.status_code == 204


@pytest.mark.asyncio
async def test_delete_job_not_user(client_app, current_user, sa_session):
    current_user.is_company = True
    sa_session.add(current_user)

    user = UserFactory.build()
    user.is_company = True
    sa_session.add(user)
    sa_session.flush()

    job = JobFactory.build()
    job.user_id = user.id
    sa_session.add(job)
    sa_session.flush()

    response = await client_app.delete(f"/jobs/delete/{job.id}")
    print(response.content)
    assert response.status_code == 403
