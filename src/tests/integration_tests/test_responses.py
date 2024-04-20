import pytest

from fixtures.jobs import JobFactory
from fixtures.responses import ResponseFactory
from fixtures.users import UserFactory
from queries import responses as responses_query
from schemas import ResponseInSchema


@pytest.mark.asyncio
async def test_create_response_job(sa_session):
    user = UserFactory.build()
    job = JobFactory.build()
    sa_session.add(user)
    sa_session.add(job)
    await sa_session.flush()

    new_response = ResponseInSchema(
        user_id=user.id, job_id=job.id, message="Hello, i'm python dev"
    )

    response_from_query = await responses_query.response_job(sa_session, new_response)

    response_check_by_id = await responses_query.get_response_by_user_id(
        sa_session, job.id
    )

    assert response_from_query
    assert response_from_query.user_id == user.id
    assert response_from_query.job_id == job.id
    assert response_from_query.message == "Hello, i'm python dev"
    assert len(response_check_by_id) == 1
    assert response_from_query == response_check_by_id[0]


@pytest.mark.asyncio
async def test_get_all_response_job(sa_session):
    new_response = ResponseFactory.build()
    sa_session.add(new_response)
    await sa_session.flush()

    response_check_by_id = await responses_query.get_response_by_user_id(
        sa_session, new_response.job_id
    )

    assert response_check_by_id
    assert len(response_check_by_id) == 1
    assert response_check_by_id[0] == new_response
