import pytest
from queries import jobs as job_query
from fixtures.users import UserFactory
from fixtures.jobs import JobFactory
from schemas import JobtoSchema



@pytest.mark.asyncio
async def test_get_all(sa_session):
    user = UserFactory.build()
    user.is_company=True
    sa_session.add(user)

    job = JobFactory.build()
    job.user_id=user.id
    sa_session.add(job)

    job = JobFactory.build()
    job.user_id=user.id
    sa_session.add(job)
    sa_session.flush()

    all_jobs = await job_query.get_all(sa_session)

    assert len(all_jobs) == 2
    assert all_jobs[1] == job


@pytest.mark.asyncio
async def test_get_by_id(sa_session):
    user = UserFactory.build()
    sa_session.add(user)
    sa_session.flush()
    user.is_company=True

    job = JobFactory.build()
    job.user_id=user.id
    sa_session.add(job)
    sa_session.flush()

    current_job = await job_query.get_by_id(sa_session, job.id)
    assert current_job is not None
    assert current_job.id == job.id

@pytest.mark.asyncio
async def test_create(sa_session):
    user = UserFactory.build()
    sa_session.add(user)
    sa_session.flush()
    user.is_company=True
    job = JobtoSchema(
        title="Naneika_Uchpochmak",
        discription="chak-chak producer",
        salary_from=500000,
        salary_to=5000000,
        is_active=True
    )

    new_job = await job_query.create(sa_session, job_schema=job,curent_user_id=user.id)
    assert new_job is not None
    assert new_job.title == "Naneika_Uchpochmak"

@pytest.mark.asyncio
async def test_update(sa_session):
    user = UserFactory.build()
    sa_session.add(user)
    sa_session.flush()
    user.is_company=True

    job = JobFactory.build()
    job.user_id=user.id
    sa_session.add(job)
    sa_session.flush()
    
    job.title="New_title"
    job= await job_query.update(sa_session, job)
    sa_session.flush()
    current_job = await job_query.get_by_id(sa_session, job.id)
    assert current_job.title =="New_title"