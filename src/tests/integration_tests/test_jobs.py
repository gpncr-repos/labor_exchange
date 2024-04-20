import datetime
from decimal import Decimal

import pytest
from pydantic import ValidationError

from fixtures.jobs import JobFactory
from fixtures.users import UserFactory
from queries import jobs as jobs_query
from schemas import JobInSchema, JobUpdateSchema


@pytest.mark.asyncio
async def test_get_all(sa_session):
    job = JobFactory.build()
    sa_session.add(job)
    await sa_session.flush()

    all_jobs = await jobs_query.get_all_jobs(sa_session)
    assert all_jobs
    assert len(all_jobs) == 1
    assert all_jobs[0] == job


@pytest.mark.asyncio
async def test_get_by_id(sa_session):
    job = JobFactory.build()
    sa_session.add(job)
    await sa_session.flush()

    response_job = await jobs_query.get_job_by_id(sa_session, job.id)
    assert response_job
    assert response_job == job


@pytest.mark.asyncio
async def test_create_job(sa_session):
    user = UserFactory.build(is_company=True)
    sa_session.add(user)
    await sa_session.flush()

    new_job = JobInSchema(
        title="Python dev",
        description="description python dev",
        salary_from=100_000.1,
        salary_to=500_000,
    )

    response_job = await jobs_query.create_job(
        sa_session, job_schema=new_job, user_id=user.id
    )

    assert response_job
    assert response_job.title == "Python dev"
    assert response_job.description == "description python dev"
    assert response_job.salary_from < response_job.salary_to
    assert response_job.salary_from == 100_000.1
    assert response_job.salary_to == 500_000
    assert response_job.is_active
    assert response_job.created_at
    assert isinstance(response_job.created_at, datetime.datetime)
    assert isinstance(response_job.is_active, bool)
    assert isinstance(response_job.salary_from, Decimal)
    assert isinstance(response_job.salary_to, Decimal)


@pytest.mark.asyncio
async def test_create_job_bad_salary(sa_session):
    user = UserFactory.build(is_company=True)
    sa_session.add(user)
    await sa_session.flush()

    with pytest.raises(ValidationError):
        new_job = JobInSchema(
            title="Python dev",
            description="description python dev",
            salary_from=500_000,
            salary_to=100_000.1,
        )

        response_job = await jobs_query.create_job(
            sa_session, job_schema=new_job, user_id=user.id
        )


@pytest.mark.asyncio
async def test_create_empty_title(sa_session):
    user = UserFactory.build(is_company=True)
    sa_session.add(user)
    await sa_session.flush()

    with pytest.raises(ValidationError):
        new_job = JobInSchema(
            title="",
            description="description python dev",
            salary_from=50_000,
            salary_to=100_000.1,
        )

        response_job = await jobs_query.create_job(
            sa_session, job_schema=new_job, user_id=user.id
        )


@pytest.mark.asyncio
async def test_create_empty_description(sa_session):
    user = UserFactory.build(is_company=True)
    sa_session.add(user)
    await sa_session.flush()

    with pytest.raises(ValidationError):
        new_job = JobInSchema(
            title="Python dev", description="", salary_from=50_000, salary_to=100_000.1
        )

        response_job = await jobs_query.create_job(
            sa_session, job_schema=new_job, user_id=user.id
        )


@pytest.mark.asyncio
async def test_delete(sa_session):
    job = JobFactory.build()
    sa_session.add(job)
    await sa_session.flush()
    del_id = job.id
    await jobs_query.delete_job(sa_session, del_id)

    deleted_job = await jobs_query.get_job_by_id(sa_session, del_id)

    assert deleted_job is None


@pytest.mark.asyncio
async def test_update_job(sa_session):
    job = JobFactory.build()
    sa_session.add(job)
    await sa_session.flush()

    new_job = JobUpdateSchema(
        title="title test",
        description="desc test",
        salary_from=100,
        salary_to=500.0,
        is_active=False,
    )

    updated_job = await jobs_query.update_job(sa_session, job.id, new_job.dict())

    assert updated_job.title == "title test"
    assert updated_job.description == "desc test"
    assert updated_job.salary_from == 100
    assert updated_job.salary_to == 500.0
    assert not updated_job.is_active


@pytest.mark.asyncio
async def test_update_job_partly(sa_session):
    job = JobFactory.build()
    sa_session.add(job)
    await sa_session.flush()

    new_job = JobUpdateSchema(description="desc test", salary_from=200, is_active=False)

    updated_job = await jobs_query.update_job(sa_session, job.id, new_job.dict())

    assert updated_job.description == "desc test"
    assert updated_job.salary_from == 200
    assert not updated_job.is_active
