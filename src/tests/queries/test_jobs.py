import pytest

from queries import jobs as job_query
from schemas import JobCreateSchema
from tests.create_obj import Conveyor


@pytest.mark.asyncio
async def test_get_all(sa_session):
    emploer = await Conveyor.create_emploer(sa_session)
    count_job = 10
    skip = 5
    limit = 8
    for _ in range(count_job):
        await Conveyor.create_job(sa_session, emploer)
    all_jobs = await job_query.get_all(sa_session, limit=limit, skip=skip)
    assert len(all_jobs) == min(count_job - skip, limit)


@pytest.mark.asyncio
async def test_get_by_id(sa_session):
    emploer = await Conveyor.create_emploer(sa_session)
    job = await Conveyor.create_job(sa_session, emploer)
    current_job = await job_query.get_by_id(sa_session, job.id)
    assert current_job
    assert current_job.id == job.id


@pytest.mark.asyncio
async def test_create(sa_session):
    emploer = await Conveyor.create_emploer(sa_session)

    job = JobCreateSchema(
        title="Naneika_Uchpochmak",
        discription="chak-chak producer",
        salary_from=500000,
        salary_to=5000000,
        is_active=True,
    )
    new_job = await job_query.create(sa_session, job_schema=job, curent_user_id=emploer.id)
    assert new_job
    assert new_job.title == "Naneika_Uchpochmak"


@pytest.mark.asyncio
async def test_update(sa_session):
    emploer = await Conveyor.create_emploer(sa_session)
    job = await Conveyor.create_job(sa_session, emploer)
    job.title = "New_title"
    job = await job_query.update(sa_session, job)
    current_job = await job_query.get_by_id(sa_session, job.id)
    assert current_job.title == "New_title"


@pytest.mark.asyncio
async def test_delete(sa_session):
    emploer = await Conveyor.create_emploer(sa_session)
    job = await Conveyor.create_job(sa_session, emploer)
    job = await job_query.delete(sa_session, job)
    current_job = await job_query.get_by_id(sa_session, job.id)
    assert not current_job
