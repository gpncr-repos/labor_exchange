import pytest
from queries import response as response_query
from fixtures.jobs import JobFactory
from fixtures.users import UserFactory
from fixtures.responses import ResponseFactory
from schemas import ResponseCreateSchema
from decimal import Decimal


@pytest.mark.asyncio
async def test_get_by_job_id(sa_session):
    user = UserFactory.build(is_company=False)
    sa_session.add(user)
    job = JobFactory.build(user_id=user.id)
    sa_session.add(job)
    await sa_session.flush()
    response = ResponseFactory.build(user_id=user.id, job_id=job.id)
    sa_session.add(response)
    await sa_session.flush()

    got_responses = await response_query.get_by_job_id(sa_session, job.id)
    assert len(got_responses) == 1
    assert got_responses[0].job_id == job.id


@pytest.mark.asyncio
async def test_create(sa_session):
    company = UserFactory.build(is_company=True)
    sa_session.add(company)
    job = JobFactory.build(user_id=company.id)
    sa_session.add(job)
    user = UserFactory.build(is_company=False)
    sa_session.add(user)
    await sa_session.flush()

    message = "Работаю как вол"

    response = ResponseCreateSchema(
        user_id=user.id,
        job_id=job.id,
        message=message,
    )

    new_response = await response_query.create(sa_session, response_schema=response)
    assert new_response is not None
    assert new_response.message == message
