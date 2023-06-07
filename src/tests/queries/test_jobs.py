import pytest
from fastapi import HTTPException

from fixtures.jobs import JobFactory
from fixtures.users import UserFactory
from queries import job as job_service

from schemas import JobInSchema


@pytest.mark.asyncio
async def test_CreateJobFromCompany_CompanyCanCreateJob_NewJobCreated(sa_session, company_user):
    job = JobInSchema(
        title='example',
        description='example',
        salary_from=100000,
        salary_to=100000
    )
    new_job = await job_service.create_job(sa_session, job_schema=job, current_user=company_user)

    assert new_job.title == job.title \
           and new_job.description == job.description \
           and new_job.salary_from == job.salary_from \
           and new_job.salary_to == job.salary_to


@pytest.mark.asyncio
async def test_CreateJobFromClient_ClientCannotCreateJob_HTTPException(sa_session, client_user):
    job = JobInSchema(
        title='example',
        description='example',
        salary_from=100000,
        salary_to=100000
    )
    with pytest.raises(HTTPException) as exc_info:
        await job_service.create_job(sa_session, job_schema=job, current_user=client_user)

    assert exc_info.value.status_code == 403
    assert exc_info.value.detail == "Только компания может создавать вакансии"


@pytest.mark.asyncio
async def test_GetAllJobs_CompanyHasMultipleJobs_ReturnsAllJobs(sa_session, company_user):

    n_jobs = 10
    jobs = []
    for _ in range(n_jobs):
        job = JobFactory.build(user_id=company_user.id)
        jobs.append(job)
        sa_session.add(job)
    sa_session.flush()

    all_jobs = await job_service.get_all_jobs(sa_session)
    assert all_jobs
    assert len(all_jobs) == n_jobs


@pytest.mark.asyncio
async def test_GetJobById_CompanyHasMultipleJobs_ReturnsJob(sa_session, company_user):

    n_jobs = 10
    jobs = []
    ids = []
    for _ in range(n_jobs):
        job = JobFactory.build(user_id=company_user.id)
        jobs.append(job)
        ids.append(job.id)
        sa_session.add(job)
    sa_session.flush()

    for i in ids:
        job = await job_service.get_job_by_id(sa_session, i)
        assert job
        assert job.id == i


@pytest.mark.asyncio
async def test_DeleteJobById_JobExists_DeletesJob(sa_session, company_user):
    n_jobs = 10
    jobs_id = []
    for _ in range(n_jobs):
        job = JobFactory.build(user_id=company_user.id)
        jobs_id.append(job.id)
        sa_session.add(job)
    sa_session.flush()

    for job in jobs_id:
        deleted_job = await job_service.delete_job_by_id(sa_session, job, company_user)
        assert deleted_job


@pytest.mark.asyncio
async def test_DeleteJobByNonExistentId_JobDoesNotExist_HTTPException(sa_session, company_user):
    with pytest.raises(HTTPException) as exc_info:
        await job_service.delete_job_by_id(sa_session, 123456, company_user)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Такой вакансии нет"


@pytest.mark.asyncio
async def test_DeleteJobAsAnotherUser_DifferentOwnerOfJob_HTTPException(sa_session, company_user):
    user = UserFactory.build()
    sa_session.add(user)
    sa_session.flush()

    job = JobFactory.build(user_id=user.id)
    sa_session.add(job)
    sa_session.flush()

    with pytest.raises(HTTPException) as exc_info:
        await job_service.delete_job_by_id(sa_session, job.id, company_user)
    assert exc_info.value.status_code == 403
    assert exc_info.value.detail == "Вы не владелец этой вакансии"
