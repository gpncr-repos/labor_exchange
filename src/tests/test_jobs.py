import pytest

from fixtures.jobs import JobFactory
from models import Job


@pytest.mark.asyncio
async def test_get_all(sa_session, job_repo):
    job = JobFactory.build()
    sa_session.add(job)
    sa_session.flush()

    all_jobs = await job_repo.get_list(sa_session)
    assert all_jobs
    assert len(all_jobs) == 1
    assert all_jobs[0] == job


@pytest.mark.asyncio
async def test_get_by_id_1(sa_session, job_repo):
    job = JobFactory.build()
    sa_session.add(job)
    sa_session.flush()

    current_job = await job_repo.get_single(sa_session, Job.id == job.id)
    assert current_job is not None
    assert current_job.id == job.id


@pytest.mark.asyncio
async def test_get_by_id_2(sa_session, job_repo):
    job = JobFactory.build()
    sa_session.add(job)
    sa_session.flush()

    current_job = await job_repo.get_single(sa_session, id=job.id)
    assert current_job is not None
    assert current_job.id == job.id
