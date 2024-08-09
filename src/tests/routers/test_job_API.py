import json

import pytest

from fixtures.jobs import JobCreateFactory
from tests.create_obj import Conveyor


@pytest.mark.asyncio
async def test_read_job_by_id(client_app, current_user, sa_session):
    count_jobs = 10
    list_of_jobs_id = []
    for _ in range(count_jobs):
        job = await Conveyor.create_job(sa_session, current_user)
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
        await Conveyor.create_job(sa_session, current_user)
    limit = 8
    skip = 5
    response = await client_app.get(f"/jobs?limit={limit}&skip={skip}")
    assert response.status_code == 200
    assert len(json.loads((response.content).decode("utf-8").replace("'", '"'))) == min(
        count_jobs - skip, limit
    )


@pytest.mark.asyncio
async def test_post_jobs_company(client_app, current_user, sa_session):
    current_user = await Conveyor.current_to_company(sa_session, current_user)
    job = (JobCreateFactory.stub()).__dict__
    response = await client_app.post("/jobs/post_job", json=job)
    assert response.status_code == 201


@pytest.mark.asyncio
async def test_post_jobs_not_company(client_app, current_user, sa_session):
    current_user = await Conveyor.current_to_worker(sa_session, current_user)
    job = (JobCreateFactory.stub()).__dict__
    response = await client_app.post("/jobs/post_job", json=job)
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_put_job_real(client_app, current_user, sa_session):
    job = await Conveyor.create_job(sa_session, current_user)
    current_user = await Conveyor.current_to_company(sa_session, current_user)
    response = await client_app.patch(
        f"/jobs/patch_job/{job.id}",
        json={"title": job.title + "_update"},
    )
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_put_job_not_company(client_app, current_user, sa_session):
    job = await Conveyor.create_job(sa_session, current_user)
    current_user = await Conveyor.current_to_worker(sa_session, current_user)
    response = await client_app.patch(
        f"/jobs/patch_job/{job.id}",
        json={"title": job.title + "_update"},
    )
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_put_job_dont_find(client_app, current_user, sa_session):
    job = await Conveyor.create_job(sa_session, current_user)
    current_user = await Conveyor.current_to_company(sa_session, current_user)
    response = await client_app.patch(
        f"/jobs/patch_job/{job.id+1}",
        json={"title": job.title + "_update"},
    )
    assert response.status_code == 204


@pytest.mark.asyncio
async def test_put_job_not_user(client_app, current_user, sa_session):
    current_user = await Conveyor.current_to_company(sa_session, current_user)
    emploer = await Conveyor.create_emploer(sa_session)
    job = await Conveyor.create_job(sa_session, emploer)

    response = await client_app.patch(
        f"/jobs/patch_job/{job.id}",
        json={"title": job.title + "_update"},
    )
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_delete_job_real(client_app, current_user, sa_session):
    job = await Conveyor.create_job(sa_session, current_user)
    current_user = await Conveyor.current_to_company(sa_session, current_user)
    response = await client_app.delete(f"/jobs/delete/{job.id}")
    assert response.status_code == 200
    response = await client_app.get(f"/jobs/{job.id}")
    assert response.status_code == 204


@pytest.mark.asyncio
async def test_delete_job_not_company(client_app, current_user, sa_session):
    job = await Conveyor.create_job(sa_session, current_user)
    current_user = await Conveyor.current_to_worker(sa_session, current_user)
    response = await client_app.delete(f"/jobs/delete/{job.id}")
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_delete_job_dont_find(client_app, current_user, sa_session):
    job = await Conveyor.create_job(sa_session, current_user)
    current_user = await Conveyor.current_to_company(sa_session, current_user)
    response = await client_app.delete(f"/jobs/delete/{job.id+1}")
    assert response.status_code == 204


@pytest.mark.asyncio
async def test_delete_job_not_user(client_app, current_user, sa_session):
    current_user = await Conveyor.current_to_company(sa_session, current_user)
    emploer = await Conveyor.create_emploer(sa_session)
    job = await Conveyor.create_job(sa_session, emploer)

    response = await client_app.delete(f"/jobs/delete/{job.id}")
    assert response.status_code == 403
