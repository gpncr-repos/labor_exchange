import pytest

from fixtures.responses import ResponseFactory
from models import Job, User, Response


@pytest.mark.asyncio
async def test_get_by_job(sa_session, response_repo):
    response = ResponseFactory.build()
    job = response.job

    sa_session.add(job)
    sa_session.add(response)
    sa_session.flush()

    fetch_response = await response_repo.get_single(sa_session, job_id=response.job_id)
    assert fetch_response is not None
    assert fetch_response.job_id == response.job_id


@pytest.mark.asyncio
async def test_get_by_job(sa_session, response_repo):
    response = ResponseFactory.build()
    user = response.user

    sa_session.add(user)
    sa_session.add(response)
    sa_session.flush()

    fetch_responses = await response_repo.get_list(sa_session, 100, 0, Response.user_id == user.id)
    assert fetch_responses
    assert len(fetch_responses) == 1
    assert fetch_responses[0].user_id == user.id
