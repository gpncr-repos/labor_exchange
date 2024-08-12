import pytest

from queries import responses as responses_query
from schemas import ResponsesCreateSchema
from tests.create_obj import Conveyor


@pytest.mark.asyncio
async def test_get_responses_by_job_id(sa_session):
    emploer = await Conveyor.create_emploer(sa_session)
    job = await Conveyor.create_job(sa_session, emploer)
    worker = await Conveyor.create_woker(sa_session)
    worker2 = await Conveyor.create_woker(sa_session)
    response = await Conveyor.create_response(sa_session, worker, job)
    response2 = await Conveyor.create_response(sa_session, worker2, job)
    all_responses = await responses_query.get_response_by_job_id(sa_session, job_id=job.id)
    assert len(all_responses) == 2
    assert all_responses[0] == response
    assert all_responses[1] == response2


@pytest.mark.asyncio
async def test_get_responses_by_user_id(sa_session):
    emploer = await Conveyor.create_emploer(sa_session)
    job = await Conveyor.create_job(sa_session, emploer)
    worker = await Conveyor.create_woker(sa_session)
    worker2 = await Conveyor.create_woker(sa_session)
    response = await Conveyor.create_response(sa_session, worker, job)
    response2 = await Conveyor.create_response(sa_session, worker2, job)
    woker_responses = await responses_query.get_response_by_user_id(sa_session, user_id=worker.id)
    woker_responses2 = await responses_query.get_response_by_user_id(sa_session, user_id=worker2.id)
    assert woker_responses[0].id == response.id
    assert woker_responses2[0].id == response2.id
    assert woker_responses[0].id != woker_responses2[0].id


@pytest.mark.asyncio
async def test_get_responses_by_id(sa_session):
    emploer = await Conveyor.create_emploer(sa_session)
    job = await Conveyor.create_job(sa_session, emploer)
    worker = await Conveyor.create_woker(sa_session)
    response = await Conveyor.create_response(sa_session, worker, job)
    woker_responses = await responses_query.get_response_by_id(sa_session, response_id=response.id)
    assert woker_responses.id == response.id


@pytest.mark.asyncio
async def test_get_responses_by_job_id_and_user_id(sa_session):
    emploer = await Conveyor.create_emploer(sa_session)
    job = await Conveyor.create_job(sa_session, emploer)
    job2 = await Conveyor.create_job(sa_session, emploer)
    worker = await Conveyor.create_woker(sa_session)
    response = await Conveyor.create_response(sa_session, worker, job)
    response2 = await Conveyor.create_response(sa_session, worker, job2)
    current_responses = await responses_query.get_response_by_job_id_and_user_id(
        sa_session, job_id=job.id, user_id=worker.id
    )
    assert current_responses.id == response.id
    assert current_responses.id != response2.id


@pytest.mark.asyncio
async def test_create(sa_session):
    emploer = await Conveyor.create_emploer(sa_session)
    job = await Conveyor.create_job(sa_session, emploer)
    worker = await Conveyor.create_woker(sa_session)
    response = ResponsesCreateSchema(
        job_id=job.id,
        message="What a beutiful job",
    )
    res = await responses_query.response_create(
        sa_session, response_schema=response, user_id=worker.id, job_id=job.id
    )
    assert res is not None
    assert res.message == "What a beutiful job"


@pytest.mark.asyncio
async def test_update(sa_session):
    emploer = await Conveyor.create_emploer(sa_session)
    job = await Conveyor.create_job(sa_session, emploer)
    worker = await Conveyor.create_woker(sa_session)
    response = await Conveyor.create_response(sa_session, worker, job)
    response.message = "New_message"
    new_response = await responses_query.update(sa_session, response)
    current_responses = await responses_query.get_response_by_id(
        sa_session, response_id=response.id
    )
    assert current_responses.id == response.id
    assert current_responses.message == "New_message"
    assert current_responses.message == new_response.message


@pytest.mark.asyncio
async def test_delete(sa_session):
    emploer = await Conveyor.create_emploer(sa_session)
    job = await Conveyor.create_job(sa_session, emploer)
    worker = await Conveyor.create_woker(sa_session)
    response = await Conveyor.create_response(sa_session, worker, job)
    new_response = await responses_query.delete(sa_session, response)
    current_responses = await responses_query.get_response_by_job_id_and_user_id(
        sa_session, job_id=job.id, user_id=worker.id
    )

    assert not current_responses
    assert new_response.id == response.id
