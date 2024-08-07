import pytest
from pydantic import ValidationError

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
