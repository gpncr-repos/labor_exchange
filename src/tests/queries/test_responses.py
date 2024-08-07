import pytest

from fixtures.jobs import JobFactory
from fixtures.responses import ResponseFactory
from fixtures.users import UserFactory
from queries import responses as responses_query
from schemas import ResponsesCreateSchema


@pytest.mark.asyncio
async def test_get_recponces_by_job_id(sa_session):
    user = UserFactory.build()
    sa_session.add(user)
    user.is_company = True

    job = JobFactory.build()
    job.user_id = user.id
    sa_session.add(job)

    worker = UserFactory.build()
    worker.is_company = False
    sa_session.add(worker)

    worker2 = UserFactory.build()
    sa_session.add(worker2)
    worker2.is_company = False

    response = ResponseFactory.build()
    response.user_id = worker.id
    response.job_id = job.id
    sa_session.add(response)

    response2 = ResponseFactory.build()
    response2.user_id = worker2.id
    response2.job_id = job.id
    sa_session.add(response2)

    sa_session.flush()

    all_responses = await responses_query.get_response_by_job_id(sa_session, job_id=job.id)

    assert len(all_responses) == 2
    assert all_responses[0] == response
    assert all_responses[1] == response2


@pytest.mark.asyncio
async def test_get_recponces_by_user_id(sa_session):
    user = UserFactory.build()
    user.is_company = True
    sa_session.add(user)

    job = JobFactory.build()
    job.user_id = user.id
    sa_session.add(job)

    worker = UserFactory.build()
    worker.is_company = False
    sa_session.add(worker)

    worker2 = UserFactory.build()
    worker2.is_company = False
    sa_session.add(worker2)

    response = ResponseFactory.build()
    response.user_id = worker.id
    response.job_id = job.id
    sa_session.add(response)

    response2 = ResponseFactory.build()
    response2.user_id = worker2.id
    response2.job_id = job.id
    sa_session.add(response2)
    sa_session.flush()

    woker_responses = await responses_query.get_response_by_user_id(sa_session, user_id=worker.id)
    woker_responses2 = await responses_query.get_response_by_user_id(sa_session, user_id=worker2.id)

    assert woker_responses[0].id == response.id
    assert woker_responses2[0].id == response2.id
    assert woker_responses[0].id != woker_responses2[0].id


@pytest.mark.asyncio
async def test_get_recponces_by_id(sa_session):
    user = UserFactory.build()
    user.is_company = True
    sa_session.add(user)

    job = JobFactory.build()
    job.user_id = user.id
    sa_session.add(job)

    worker = UserFactory.build()
    worker.is_company = False
    sa_session.add(worker)

    response = ResponseFactory.build()
    response.user_id = worker.id
    response.job_id = job.id
    sa_session.add(response)

    sa_session.flush()

    woker_responses = await responses_query.get_response_by_id(sa_session, response_id=response.id)

    assert woker_responses.id == response.id


@pytest.mark.asyncio
async def test_get_recponces_by_job_id_and_user_id(sa_session):
    user = UserFactory.build()
    user.is_company = True
    sa_session.add(user)

    job = JobFactory.build()
    job.user_id = user.id
    sa_session.add(job)

    worker = UserFactory.build()
    worker.is_company = False
    sa_session.add(worker)

    response = ResponseFactory.build()
    response.user_id = worker.id
    response.job_id = job.id
    sa_session.add(response)

    response2 = ResponseFactory.build()
    response2.user_id = worker.id
    response2.job_id = job.id
    sa_session.add(response2)
    sa_session.flush()

    current_responses = await responses_query.get_response_by_job_id_and_user_id(
        sa_session, job_id=job.id, user_id=user.id
    )

    assert current_responses.id == response.id
    assert current_responses.id != response2.id


@pytest.mark.asyncio
async def test_create(sa_session):
    user = UserFactory.build()
    user.is_company = True
    sa_session.add(user)

    job = JobFactory.build()
    job.user_id = user.id
    sa_session.add(job)

    worker = UserFactory.build()
    user.is_company = False
    sa_session.add(worker)

    sa_session.flush()

    response = ResponsesCreateSchema(
        job_id=job.id,
        message="What a beutiful job",
    )

    res = await responses_query.response_create(
        sa_session, response_schema=response, user_id=worker.id
    )
    assert res is not None
    assert res.message == "What a beutiful job"


@pytest.mark.asyncio
async def test_update(sa_session):
    user = UserFactory.build()
    user.is_company = True
    sa_session.add(user)

    job = JobFactory.build()
    job.user_id = user.id
    sa_session.add(job)

    worker = UserFactory.build()
    worker.is_company = False
    sa_session.add(worker)

    response = ResponseFactory.build()
    response.user_id = worker.id
    response.job_id = job.id
    sa_session.add(response)
    sa_session.flush()
    response.message = "New_message"

    new_response = await responses_query.update(sa_session, response)
    current_responses = await responses_query.get_response_by_job_id_and_user_id(
        sa_session, job_id=job.id, user_id=worker.id
    )

    assert current_responses.id == response.id
    assert current_responses.message == "New_message"
    assert current_responses.message == new_response.message


@pytest.mark.asyncio
async def test_delete(sa_session):
    user = UserFactory.build()
    user.is_company = True
    sa_session.add(user)

    job = JobFactory.build()
    job.user_id = user.id
    sa_session.add(job)

    worker = UserFactory.build()
    worker.is_company = False
    sa_session.add(worker)

    response = ResponseFactory.build()
    response.user_id = worker.id
    response.job_id = job.id
    sa_session.add(response)

    sa_session.flush()

    new_response = await responses_query.delete(sa_session, response)
    current_responses = await responses_query.get_response_by_job_id_and_user_id(
        sa_session, job_id=job.id, user_id=worker.id
    )

    assert current_responses is None
    assert new_response.id == response.id
