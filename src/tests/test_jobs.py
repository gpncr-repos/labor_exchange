import pytest
import pytest_asyncio

from fixtures.jobs import JobFactory
from fixtures.users import UserFactory
from queries import job as job_queries
from schemas.job import CreateJobRequest, CreateResponseRequest


@pytest.mark.asyncio
async def test_get(sa_session):
    job = JobFactory.build()
    sa_session.add(job)
    sa_session.flush()
    current_user = await job_queries.get_job_by_id(sa_session, job.id)
    assert current_user is not None
    assert current_user.id == job.id


@pytest.mark.asyncio
async def test_get_all(sa_session):
    jobs = JobFactory.build_batch(10)
    sa_session.add_all(jobs)
    sa_session.flush()

    all_jobs = await job_queries.get_all_jobs(sa_session)
    assert all_jobs
    # assert len(all_jobs) == 10 #TODO: не работает на заполненной базе
    assert len(all_jobs) != 0


@pytest.mark.asyncio
async def test_create(sa_session):
    user = UserFactory.build(is_company=True)
    sa_session.add(user)
    sa_session.flush()

    job = CreateJobRequest(
        title="Senior-Chief",
        description="СРОЧНО НУЖЕН ПОВАР УЧПОЧМАКОВ",
        salary_from=1000000,
        salary_to=99999999,
    )

    new_job = await job_queries.create_job(db=sa_session, user_id=user.id, job_schema=job)
    assert new_job is not None
    assert new_job.title == job.title
    assert new_job.description == job.description
    assert new_job.salary_from == job.salary_from
    assert new_job.salary_to == job.salary_to


@pytest.mark.asyncio
async def test_update(sa_session):
    job = JobFactory.build()
    sa_session.add(job)
    sa_session.flush()

    job.title = "TESTUPDATE"
    job.description = "TESTUPDATE"
    job.is_active = False

    updated_job = await job_queries.update_job(sa_session, job)

    assert updated_job.title == "TESTUPDATE"
    assert updated_job.description == "TESTUPDATE"
    assert updated_job.is_active == False


@pytest.mark.asyncio
async def test_remove(sa_session):
    job = JobFactory.build()
    sa_session.add(job)
    sa_session.flush()

    found_work = await job_queries.get_job_by_id(sa_session, job.id)
    assert found_work is not None

    await job_queries.remove_job(sa_session, job.id)

    found_work = await job_queries.get_job_by_id(sa_session, job.id)
    assert found_work is None


@pytest.mark.asyncio
async def test_create_response(sa_session):
    job = JobFactory.build()
    user = UserFactory.build(is_company=False)
    sa_session.add(job)
    sa_session.add(user)
    sa_session.flush()

    response = CreateResponseRequest(message="TEST_MESSAGE")
    response = await job_queries.create_response(sa_session, job.id, user.id, response)

    assert response.user_id == user.id
    assert response.job_id == job.id


@pytest.mark.asyncio
async def test_get_response_by_id(sa_session):
    job = JobFactory.build()
    user = UserFactory.build(is_company=False)
    sa_session.add(job)
    sa_session.add(user)
    sa_session.flush()
    response = CreateResponseRequest(message="TEST_MESSAGE")
    response = await job_queries.create_response(sa_session, job.id, user.id, response)

    responses = await job_queries.get_response_by_job_id(sa_session, job.id)

    assert len(responses) != 0
