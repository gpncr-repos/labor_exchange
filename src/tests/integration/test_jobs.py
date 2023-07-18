from decimal import Decimal

import pytest
from pydantic import ValidationError

from factories.jobs import JobFactory
from factories.users import UserFactory
from queries import job as job_query
from schemas import JobCreateSchema, JobUpdateSchema


@pytest.mark.asyncio
async def test_get_all(sa_session):
    job = JobFactory.build()
    sa_session.add(job)
    sa_session.flush()

    all_jobs = await job_query.get_all(sa_session)
    assert all_jobs
    assert len(all_jobs) == 1
    assert all_jobs[0] == job
    assert all_jobs[0].user
    assert all_jobs[0].user.is_company


@pytest.mark.asyncio
async def test_get_by_id(sa_session):
    job = JobFactory.build()
    sa_session.add(job)
    sa_session.flush()

    current_job = await job_query.get_by_id(sa_session, job.id)
    assert current_job is not None
    assert current_job.id == job.id


@pytest.mark.asyncio
async def test_create(sa_session):
    user = UserFactory.build(is_company=True)
    sa_session.add(user)
    sa_session.flush()

    job = JobCreateSchema(
        title="Job title",
        description="Job description",
        salary_from=200_000.45,
        salary_to=300_500.79,
        is_active=True
    )

    new_job = await job_query.create(sa_session, job, creator_id=user.id)
    assert new_job is not None
    assert new_job.title == "Job title"
    assert new_job.description == "Job description"
    assert isinstance(new_job.salary_from, Decimal)
    assert isinstance(new_job.salary_to, Decimal)
    assert new_job.salary_from > 100_000
    assert new_job.salary_to < 400_000
    assert new_job.is_active
    assert new_job.user.is_company


@pytest.mark.asyncio
async def test_create_negative_salary(sa_session):
    user = UserFactory.build(is_company=True)
    sa_session.add(user)
    sa_session.flush()

    with pytest.raises(ValidationError):
        job = JobCreateSchema(
            title="Job title",
            description="Job description",
            salary_from=-300,
            salary_to=-100,
            is_active=True
        )

        await job_query.create(sa_session, job, creator_id=user.id)


@pytest.mark.asyncio
async def test_create_incorrect_salary_range(sa_session):
    user = UserFactory.build(is_company=True)
    sa_session.add(user)
    sa_session.flush()

    with pytest.raises(ValidationError):
        job = JobCreateSchema(
            title="Job title",
            description="Job description",
            salary_from=50_000,
            salary_to=20_000,
            is_active=True
        )

        await job_query.create(sa_session, job, creator_id=user.id)


@pytest.mark.asyncio
async def test_create_incorrect_salary_places_after_dot(sa_session):
    user = UserFactory.build(is_company=True)
    sa_session.add(user)
    sa_session.flush()

    with pytest.raises(ValidationError):
        job = JobCreateSchema(
            title="Job title",
            description="Job description",
            salary_from=100_000.254,
            salary_to=300_000.657,
            is_active=True
        )

        await job_query.create(sa_session, job, creator_id=user.id)


@pytest.mark.asyncio
async def test_update(sa_session):
    job = JobFactory.build()
    sa_session.add(job)
    sa_session.flush()

    update_schema = JobUpdateSchema(
        title="Updated title",
        description="Updated description",
        salary_from=20_000,
        salary_to=30_000,
        is_active=True
    )

    updated_job = await job_query.update(sa_session, job, update_schema)
    assert updated_job.title == "Updated title"
    assert updated_job.description == "Updated description"
    assert updated_job.salary_from == 20_000
    assert updated_job.salary_to == 30_000
    assert updated_job.is_active


@pytest.mark.asyncio
async def test_update_partial(sa_session):
    job = JobFactory.build()
    sa_session.add(job)
    sa_session.flush()

    update_schema = JobUpdateSchema(
        title="Just new title"
    )

    updated_job = await job_query.update(sa_session, job, update_schema)
    assert updated_job.title == "Just new title"


@pytest.mark.asyncio
async def test_update_no_both_salary_edges(sa_session):
    job = JobFactory.build()
    sa_session.add(job)
    sa_session.flush()

    with pytest.raises(ValidationError):
        update_schema = JobUpdateSchema(
            salary_to=30_000
        )
        await job_query.update(sa_session, job, update_schema)


@pytest.mark.asyncio
async def test_delete(sa_session):
    job = JobFactory.build()
    sa_session.add(job)
    sa_session.flush()

    deleted_job_id = job.id

    await job_query.delete(sa_session, job)
    deleted_job = await job_query.get_by_id(sa_session, deleted_job_id)
    assert deleted_job is None
