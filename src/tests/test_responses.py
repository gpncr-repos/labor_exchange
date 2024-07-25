import pytest
from queries import responses as responses_query
from fixtures.users import UserFactory
from fixtures.jobs import JobFactory
from fixtures.responses import ResponseFactory
from schemas import ResponsesinSchema


@pytest.mark.asyncio
async def test_get_recponces_by_job_id_and_user_id(sa_session):
    user = UserFactory.build()
    sa_session.add(user)
    sa_session.flush()
    user.is_company=True

    job = JobFactory.build()
    job.user_id=user.id
    sa_session.add(job)
    sa_session.flush()

    worker = UserFactory.build()
    sa_session.add(worker)
    sa_session.flush()
    user.is_company=False

    response = ResponseFactory.build()
    response.user_id=worker.id
    response.job_id=job.id
    sa_session.add(response)
    sa_session.flush()

    all_responses = await responses_query.get_response_by_job_id_and_user_id(sa_session,job_id=job.id,user_id=user.id)

    assert len(all_responses) == 1
    assert all_responses[0] == response

@pytest.mark.asyncio
async def test_get_recponces_by_job_id_and_user_id(sa_session):
    user = UserFactory.build()
    sa_session.add(user)
    sa_session.flush()
    user.is_company=True

    job = JobFactory.build()
    job.user_id=user.id
    sa_session.add(job)
    sa_session.flush()

    worker = UserFactory.build()
    sa_session.add(worker)
    sa_session.flush()
    user.is_company=False

    worker2 = UserFactory.build()
    sa_session.add(worker2)
    sa_session.flush()
    user.is_company=False

    response = ResponseFactory.build()
    response.user_id=worker.id
    response.job_id=job.id
    sa_session.add(response)
    sa_session.flush()

    response2= ResponseFactory.build()
    response2.user_id=worker2.id
    response2.job_id=job.id
    sa_session.add(response2)
    sa_session.flush()

    all_responses = await responses_query.get_response_by_job_id(sa_session,job_id=job.id)

    assert len(all_responses) == 2
    assert all_responses[1] == response2

@pytest.mark.asyncio
async def test_create(sa_session):
    user = UserFactory.build()
    sa_session.add(user)
    sa_session.flush()
    user.is_company=True

    job = JobFactory.build()
    job.user_id=user.id
    sa_session.add(job)
    sa_session.flush()

    worker = UserFactory.build()
    sa_session.add(worker)
    sa_session.flush()
    user.is_company=False

    response = ResponsesinSchema(
        job_id=job.id,
        massage="What a beutiful job",

    )

    response = await responses_query.response_create(sa_session,response_schema=response,user_id=worker.id)
    assert response is not None
    assert response.massage =="What a beutiful job"
