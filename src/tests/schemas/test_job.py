import pytest
from pydantic import ValidationError

from fixtures.jobs import JobFactory
from fixtures.users import UserFactory
from queries import jobs as job_query
from schemas import JobCreateSchema


@pytest.mark.asyncio
async def test_create_salary_mistake_lt(sa_session):
    with pytest.raises(ValidationError):
        user = UserFactory.build()
        sa_session.add(user)
        sa_session.flush()
        user.is_company = True
        job = JobCreateSchema(
            title="Naneika_Uchpochmak",
            discription="chak-chak producer",
            salary_from=500000,
            salary_to=5000,
            is_active=True,
        )
        await job_query.create(sa_session, job_schema=job, curent_user_id=user.id)


@pytest.mark.asyncio
async def test_create_salary_mistake_salary_to_lt_salary_from(sa_session):
    with pytest.raises(ValidationError):
        user = UserFactory.build()
        sa_session.add(user)
        sa_session.flush()
        user.is_company = True
        job = JobCreateSchema(
            title="Naneika_Uchpochmak",
            discription="chak-chak producer",
            salary_from=-500000,
            salary_to=5000,
            is_active=True,
        )
        await job_query.create(sa_session, job_schema=job, curent_user_id=user.id)


@pytest.mark.asyncio
async def test_update_salary_mistake_salary_to_lt_salary_from(sa_session):
    with pytest.raises(ValidationError):
        user = UserFactory.build()
        sa_session.add(user)
        user.is_company = True
        job = JobFactory.build()
        job = await job_query.create(sa_session, job_schema=job, curent_user_id=user.id)
        sa_session.flush()
        job.salary_from = job.salary_from
        job.salary_to = job.salary_from - 1
        await job_query.update(sa_session, update_job=job)


@pytest.mark.asyncio
async def test_update_salary_mistake_salary_from_lt_0(sa_session):
    with pytest.raises(ValidationError):
        user = UserFactory.build()
        sa_session.add(user)
        sa_session.flush()
        user.is_company = True
        job = JobFactory.build()
        job = await job_query.create(sa_session, job_schema=job, curent_user_id=user.id)
        sa_session.flush()
        job.salary_from = -10000
        await job_query.update(sa_session, update_job=job)
