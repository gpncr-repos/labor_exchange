import pytest
from queries import job as job_query
from fixtures.jobs import JobFactory
from schemas import JobCreateSchema
from fixtures.users import UserFactory
from decimal import Decimal


@pytest.mark.asyncio
async def test_get_all(sa_session):
    user = UserFactory.build()
    sa_session.add(user)
    job = JobFactory.build(user_id=user.id)
    sa_session.add(job)
    await sa_session.flush()

    all_jobs = await job_query.get_all(sa_session)
    assert all_jobs
    assert len(all_jobs) == 1
    assert all_jobs[0] == job


@pytest.mark.asyncio
async def test_get_by_id(sa_session):
    user = UserFactory.build()
    sa_session.add(user)
    job = JobFactory.build(user_id=user.id)
    sa_session.add(job)
    await sa_session.flush()

    got_job = await job_query.get_by_id(sa_session, job.id)
    assert got_job is not None
    assert got_job.id == job.id


@pytest.mark.asyncio
async def test_get_by_id_single(sa_session):
    user = UserFactory.build()
    sa_session.add(user)
    job_1 = JobFactory.build(user_id=user.id)
    sa_session.add(job_1)
    job_2 = JobFactory.build(user_id=user.id)
    sa_session.add(job_2)
    await sa_session.flush()

    got_job = await job_query.get_by_id(sa_session, job_1.id)
    assert got_job is not None
    assert got_job.id == job_1.id

    got_job = await job_query.get_by_id(sa_session, job_2.id)
    assert got_job is not None
    assert got_job.id == job_2.id


@pytest.mark.asyncio
async def test_create(sa_session):
    user = UserFactory.build(is_company=True)
    sa_session.add(user)

    title = "Работа"
    value = Decimal("100.23")

    job = JobCreateSchema(
        user_id=user.id,
        title=title,
        description="Хорошая работа",
        salary_from=value,
        salary_to=Decimal("110.56"),
        is_active=True,
    )

    new_job = await job_query.create(sa_session, job_schema=job)
    assert new_job is not None
    assert new_job.title == title
    assert new_job.salary_from == value
