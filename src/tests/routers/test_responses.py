import pytest
from pydantic import ValidationError
from starlette import status

from fixtures.jobs import JobFactory
from fixtures.responses import ResponseFactory
from fixtures.users import UserFactory
from schemas import ResponseInSchema, JobInSchema


@pytest.mark.asyncio
async def test_GetResponseByUserId_JobAndResponsesExist_ReturnsAllResponses(sa_session, http_client, company_user):
    new_job = JobFactory.build()
    new_job.user_id = company_user.id
    sa_session.add(new_job)
    sa_session.flush()

    responses = []
    n_responses = 10
    for _ in range(n_responses):
        response = ResponseFactory.build(user_id=company_user.id)
        response.job_id = new_job.id

        sa_session.add(response)
        responses.append(response)
    sa_session.flush()

    all_responses = await http_client.get(url=f'/responses/user-id/{company_user.id}')
    assert len(all_responses.json()) == n_responses

    for i, response in enumerate(responses):
        assert all_responses.json()[i]['id'] == response.id \
               and all_responses.json()[i]['job_id'] == response.job_id \
               and all_responses.json()[i]['user_id'] == response.user_id \
               and all_responses.json()[i]['message'] == response.message


@pytest.mark.asyncio
async def test_GetResponseByJobId_JobAndResponsesExist_ReturnsAllResponses(sa_session, http_client, company_user):
    new_job = JobFactory.build()
    new_job.user_id = company_user.id
    sa_session.add(new_job)
    sa_session.flush()

    responses = []
    n_responses = 10
    for _ in range(n_responses):
        response = ResponseFactory.build(user_id=company_user.id)
        response.job_id = new_job.id

        sa_session.add(response)
        responses.append(response)
    sa_session.flush()

    all_responses = await http_client.get(url=f'/responses/job-id/{new_job.id}')
    assert len(all_responses.json()) == n_responses

    for i, response in enumerate(responses):
        assert all_responses.json()[i]['id'] == response.id \
               and all_responses.json()[i]['job_id'] == response.job_id \
               and all_responses.json()[i]['user_id'] == response.user_id \
               and all_responses.json()[i]['message'] == response.message


@pytest.mark.asyncio
async def test_CreateResponseAsClient_ValidJobAndUser_CreatesNewResponse(sa_session, http_client, undefined_user, company_user):
    new_job = JobFactory.build(user_id=company_user.id, is_active=True)
    sa_session.add(new_job)
    sa_session.flush()

    client_user = undefined_user
    client_user.is_company = False
    sa_session.add(client_user)
    sa_session.flush()

    new_response = ResponseFactory.build()
    sa_session.add(new_response)
    sa_session.flush()

    response_schema = ResponseInSchema(
        job_id=new_job.id,
        message=new_response.message
    )

    created_response = await http_client.post(url='/responses', json=response_schema.dict())

    assert created_response.json()['message'] == new_response.message


@pytest.mark.asyncio
async def test_CreateResponseAsClient_ResponseAlreadyExists_ReturnsBadRequestError(sa_session, http_client, undefined_user, company_user):
    new_job = JobFactory.build(user_id=company_user.id, is_active=True)
    sa_session.add(new_job)
    sa_session.flush()

    client_user = undefined_user
    client_user.is_company = False
    sa_session.add(client_user)
    sa_session.flush()

    new_response = ResponseFactory.build()
    sa_session.add(new_response)
    sa_session.flush()

    response_schema = ResponseInSchema(
        job_id=new_job.id,
        message=new_response.message
    )

    created_response = await http_client.post(url='/responses', json=response_schema.dict())

    assert created_response.json()['message'] == new_response.message

    created_response = await http_client.post(url='/responses', json=response_schema.dict())

    assert created_response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.asyncio
async def test_CreateResponseAsNotClient_ValidJobAndUser_ReturnsForbiddenError(sa_session, http_client, undefined_user, company_user):
    new_job = JobFactory.build(user_id=company_user.id, is_active=True)
    sa_session.add(new_job)
    sa_session.flush()

    client_user = undefined_user
    client_user.is_company = True
    sa_session.add(client_user)
    sa_session.flush()

    new_response = ResponseFactory.build()
    sa_session.add(new_response)
    sa_session.flush()

    response_schema = ResponseInSchema(
        job_id=new_job.id,
        message=new_response.message
    )

    created_response = await http_client.post(url='/responses', json=response_schema.dict())

    assert created_response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.asyncio
async def test_DeleteResponseById_ResponseDoesNotExist_ReturnsNotFoundError(sa_session, http_client, undefined_user, company_user):
    new_job = JobFactory.build(user_id=company_user.id, is_active=True)
    sa_session.add(new_job)
    sa_session.flush()

    client_user = undefined_user
    client_user.is_company = False
    sa_session.add(client_user)
    sa_session.flush()

    new_response = ResponseFactory.build()
    sa_session.add(new_response)
    sa_session.flush()

    response_schema = ResponseInSchema(
        job_id=new_job.id,
        message=new_response.message
    )

    created_response = await http_client.post(url='/responses', json=response_schema.dict())
    created_response_id = created_response.json()['id']

    deleted_response = await http_client.delete(url=f'/responses/{created_response_id}')

    assert deleted_response.json() == True

    deleted_response = await http_client.delete(url=f'/responses/{created_response_id}')

    assert deleted_response.status_code == status.HTTP_404_NOT_FOUND

@pytest.mark.asyncio
async def test_DeleteResponseOtherUser_DifferentOwnerOfResponse_ReturnsForbiddenError(sa_session, http_client, undefined_user):
    user = UserFactory.build()
    sa_session.add(user)
    sa_session.flush()

    new_job = JobFactory.build(user_id=user.id, is_active=True)
    sa_session.add(new_job)
    sa_session.flush()

    client_user = undefined_user
    client_user.is_company = False
    sa_session.add(client_user)
    sa_session.flush()

    deleted_job = await http_client.delete(url=f'/jobs/{new_job.id}')

    assert deleted_job.status_code == status.HTTP_403_FORBIDDEN