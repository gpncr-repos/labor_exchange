import pytest

from factories.responses import ResponseFactory
from factories.jobs import JobFactory
from factories.users import UserFactory
from schemas import ResponseCreateSchema
from queries import response as response_query


@pytest.mark.asyncio
async def test_get_all_by_job_id(sa_session):
    response = ResponseFactory.build()
    sa_session.add(response)
    sa_session.flush()

    all_responses = await response_query.get_responses_by_job_id(sa_session, response.job.id)
    assert all_responses
    assert len(all_responses) == 1
    assert all_responses[0] == response
    assert not all_responses[0].user.is_company
    assert all_responses[0].job.user.is_company


@pytest.mark.asyncio
async def test_response_job(sa_session):
    response_schema = ResponseCreateSchema(
        message="Hi, this is my response to the job"
    )

    user = UserFactory.build(is_company=False)
    job = JobFactory.build()
    sa_session.add_all((user, job))
    sa_session.flush()

    response = await response_query.response_job(sa_session, job.id, response_schema, user.id)
    assert response.message == "Hi, this is my response to the job"
    assert response.job == job
    assert response.user == user
