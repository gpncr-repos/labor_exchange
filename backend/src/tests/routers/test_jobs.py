import pytest
from starlette import status

from fixtures.jobs import JobFactory
from fixtures.users import UserFactory
from schemas import JobInSchema

import random


def generate_random_salary_range():
    salary_from = random.randint(1, 1000000)
    salary_to = random.randint(salary_from, 1000000)
    return salary_from, salary_to


@pytest.mark.asyncio
async def test_GetJobs_MultipleJobsExist_ReturnsAllJobs(sa_session, http_client, company_user):
    n_jobs = 10
    for _ in range(n_jobs):
        salary_from, salary_to = generate_random_salary_range()

        new_job = JobFactory.build(user_id=company_user.id, salary_from=salary_from, salary_to=salary_to)
        sa_session.add(new_job)
    sa_session.flush()

    all_jobs = await http_client.get('/jobs')
    assert len(all_jobs.json()) == n_jobs


@pytest.mark.asyncio
async def test_GetJobById_JobExists_ReturnsSpecificJob(sa_session, http_client, company_user):
    salary_from, salary_to = generate_random_salary_range()

    new_job = JobFactory.build(user_id=company_user.id, salary_from=salary_from, salary_to=salary_to)
    sa_session.add(new_job)
    sa_session.flush()

    job = await http_client.get(f'/jobs/{new_job.id}')
    assert job.json()['id'] == new_job.id \
           and job.json()['title'] == new_job.title \
           and job.json()['description'] == new_job.description


# ОШИБКА
@pytest.mark.asyncio
async def test_CreateJobAsCompany_UserIsCompany_CreatesNewJob(sa_session, http_client, undefined_user):
    company_user = undefined_user
    company_user.is_company = True
    sa_session.add(company_user)
    sa_session.flush()

    salary_from, salary_to = generate_random_salary_range()

    new_job = JobFactory.build(salary_from=salary_from, salary_to=salary_to)
    sa_session.add(new_job)
    sa_session.flush()

    job_schema = JobInSchema(
        title=new_job.title,
        description=new_job.description,
        salary_from=new_job.salary_from,
        salary_to=new_job.salary_to
    )

    created_job = await http_client.post(url='/jobs', json=job_schema.dict())

    assert created_job.json()["title"] == new_job.title \
           and created_job.json()["description"] == new_job.description \
           and created_job.json()["salary_from"] == new_job.salary_from \
           and created_job.json()["salary_to"] == new_job.salary_to


@pytest.mark.asyncio
async def test_CreateJobAsNotCompany_UserIsNotCompany_ReturnsForbiddenError(sa_session, http_client, undefined_user):
    client_user = undefined_user
    client_user.is_company = False
    sa_session.add(client_user)
    sa_session.flush()

    salary_from, salary_to = generate_random_salary_range()

    new_job = JobFactory.build(salary_from=salary_from, salary_to=salary_to)
    sa_session.add(new_job)
    sa_session.flush()

    job_schema = JobInSchema(
        title=new_job.title,
        description=new_job.description,
        salary_from=new_job.salary_from,
        salary_to=new_job.salary_to
    )

    created_job = await http_client.post(url='/jobs', json=job_schema.dict())

    assert created_job.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.asyncio
async def test_DeleteJob_JobExists_DeletesJob(sa_session, http_client, undefined_user):
    company_user = undefined_user
    company_user.is_company = True
    sa_session.add(company_user)
    sa_session.flush()

    salary_from, salary_to = generate_random_salary_range()

    new_job = JobFactory.build(salary_from=salary_from, salary_to=salary_to)
    sa_session.add(new_job)
    sa_session.flush()

    job_schema = JobInSchema(
        title=new_job.title,
        description=new_job.description,
        salary_from=new_job.salary_from,
        salary_to=new_job.salary_to
    )

    created_job = await http_client.post(url='/jobs', json=job_schema.dict())
    created_job_id = created_job.json()['id']

    deleted_job = await http_client.delete(url=f'/jobs/{created_job_id}')

    assert deleted_job.json() == True

    deleted_job = await http_client.delete(url=f'/jobs/{created_job_id}')

    assert deleted_job.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_DeleteJobOtherUser_DifferentOwnerOfJob_ReturnsForbiddenError(sa_session, http_client, undefined_user):
    user = UserFactory.build()
    sa_session.add(user)
    sa_session.flush()

    salary_from, salary_to = generate_random_salary_range()

    new_job = JobFactory.build(user_id=user.id, salary_from=salary_from, salary_to=salary_to)
    sa_session.add(new_job)
    sa_session.flush()

    company_user = undefined_user
    company_user.is_company = True
    sa_session.add(company_user)
    sa_session.flush()

    deleted_job = await http_client.delete(url=f'/jobs/{new_job.id}')

    assert deleted_job.status_code == status.HTTP_403_FORBIDDEN
