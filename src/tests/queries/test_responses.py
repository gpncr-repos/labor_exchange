import pytest
from fastapi import HTTPException

from fixtures.jobs import JobFactory
from fixtures.responses import ResponseFactory
from fixtures.users import UserFactory
from queries.response import get_responses_by_user_id
from schemas import ResponseInSchema
from queries import response as response_service


@pytest.mark.asyncio
async def test_CreateResponseFromClient_JobIsActive_NewResponseCreated(sa_session, company_user, client_user):
    job = JobFactory.build(user_id=company_user.id)
    job.is_active = True
    sa_session.add(job)
    sa_session.flush()

    response = ResponseInSchema(
        job_id=job.id,
        message='example'
    )

    new_response = await response_service.create_response(sa_session, response_schema=response,
                                                          current_user=client_user)

    assert new_response.job_id == response.job_id \
           and new_response.message == response.message \
           and new_response.user_id == client_user.id


@pytest.mark.asyncio
async def test_CreateResponseFromCompany_JobIsActive_HTTPException(sa_session, company_user):
    user = UserFactory.build()
    sa_session.add(user)
    sa_session.flush()

    job = JobFactory.build(user_id=user.id, is_active=True)
    sa_session.add(job)
    sa_session.flush()

    response = ResponseInSchema(
        job_id=job.id,
        message='example'
    )

    with pytest.raises(HTTPException) as exc_info:
        await response_service.create_response(sa_session, response_schema=response, current_user=company_user)

    assert exc_info.value.status_code == 403
    assert exc_info.value.detail == "Компании не могут оставлять отклик"


@pytest.mark.asyncio
async def test_CreateResponseToInactiveJob_JobIsInactive_HTTPException(sa_session, company_user, client_user):
    job = JobFactory.build(user_id=company_user.id, is_active=False)
    sa_session.add(job)
    sa_session.flush()

    response = ResponseInSchema(
        job_id=job.id,
        message='example'
    )

    with pytest.raises(HTTPException) as exc_info:
        await response_service.create_response(sa_session, response_schema=response, current_user=client_user)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Такой вакансии нет или она не активна"


@pytest.mark.asyncio
async def test_GetResponseByUserId_JobExists_ReturnsClientResponses(sa_session, company_user, client_user):
    n_jobs = 10
    jobs = []
    for _ in range(n_jobs):
        job = JobFactory.build(user_id=company_user.id, is_active=True)
        jobs.append(job)
        sa_session.add(job)
    sa_session.flush()

    responses = []
    for job in jobs:
        response = ResponseFactory.build(user_id=client_user.id, job_id=job.id)
        sa_session.add(response)
        responses.append(response)
    sa_session.flush()
    client_responses = await response_service.get_responses_by_user_id(sa_session, user_id=client_user.id)

    assert client_responses
    assert len(client_responses) == 10


@pytest.mark.asyncio
async def test_GetResponseByJobId_JobExists_ReturnsJobResponses(sa_session, company_user, client_user):
    job = JobFactory.build(user_id=company_user.id, is_active=True)
    sa_session.add(job)
    sa_session.flush()

    n_responses = 10

    for _ in range(n_responses):
        response = ResponseFactory.build(user_id=client_user.id, job_id=job.id)
        sa_session.add(response)
    sa_session.flush()
    job_responses = await response_service.get_responses_by_job_id(sa_session, job_id=job.id)

    assert job_responses
    assert len(job_responses) == 10


@pytest.mark.asyncio
async def test_DeleteResponseById_ResponseExists_DeletesResponse(sa_session, company_user, client_user):
    job = JobFactory.build(user_id=company_user.id, is_active=True)
    sa_session.add(job)
    sa_session.flush()

    n_responses = 10
    responses = []
    for _ in range(n_responses):
        response = ResponseFactory.build(user_id=client_user.id, job_id=job.id)
        responses.append(response)
        sa_session.add(response)
    sa_session.flush()

    assert len(await get_responses_by_user_id(sa_session, client_user.id)) == 10

    for response in responses:
        job_responses = await response_service.delete_response_by_id(sa_session, response_id=response.id,
                                                                     current_user=client_user)
        assert job_responses

    assert len(await get_responses_by_user_id(sa_session, client_user.id)) == 0


@pytest.mark.asyncio
async def test_DeleteResponseByNonExistentId_ResponseDoesNotExist_HTTPException(sa_session, client_user):
    with pytest.raises(HTTPException) as exc_info:
        await response_service.delete_response_by_id(sa_session, 123456, client_user)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Такого отклика нет"


@pytest.mark.asyncio
async def test_DeleteResponseAsAnotherUser_DifferentOwnerOfResponse_HTTPException(sa_session, company_user,
                                                                                  client_user):
    user = UserFactory.build()
    sa_session.add(user)
    sa_session.flush()

    job = JobFactory.build(user_id=company_user.id)
    sa_session.add(job)
    sa_session.flush()

    response = ResponseFactory.build(user_id=user.id, job_id=job.id)
    sa_session.add(response)

    with pytest.raises(HTTPException) as exc_info:
        await response_service.delete_response_by_id(sa_session, response.id, client_user)
    assert exc_info.value.status_code == 403
    assert exc_info.value.detail == "Вы не владелец этого отклика"
