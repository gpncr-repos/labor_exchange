import json
from datetime import datetime
from decimal import Decimal

import pytest
from sqlalchemy import select

import models
from api.schemas import UserInSchema, UserUpdateSchema
from api.schemas.job_schemas import SJob
from core.security import hash_password
from domain.dm_schemas import DMUser
from infrastructure.repos import RepoUser


@pytest.mark.asyncio
async def test_add_user(client_app, sa_session):
    """Тест эндпоинта создания пользователя"""
    # ARRANGE
    user_to_add = UserInSchema(
        name="TestUser",
        email="TestUser@email.com",
        password="TestUserSomePass",
        password2="TestUserSomePass",
        is_company=False,
    )
    # ACT
    request_add_user = await client_app.post(url="/users", json=user_to_add.dict())
    # ASSERT
    assert request_add_user.status_code == 200, "Ошибка при создании пользователя"


@pytest.mark.asyncio
async def test_read_users1(client_app, sa_session):
    """Тест эндпоинта получения списка пользователей"""
    # ASSERT
    user_to_add = UserInSchema(
        name="TestUser",
        email="TestUser@email.com",
        password="TestUserSomePass",
        password2="TestUserSomePass",
        is_company=False,
    )
    request_add_user = await client_app.post(url="/users", json=user_to_add.dict())
    assert request_add_user.status_code == 200, "Ошибка при создании пользователя"
    # ACT
    request_read = await client_app.get(url="/users")
    # ASSERT
    assert request_read.status_code == 200, "Не удалось получить список пользователей"


@pytest.mark.asyncio
async def test_read_users2(client_app, sa_session):
    """Тест эндпоинта получения списка пользователей"""
    # ARRANGE
    repo_user = RepoUser(sa_session)
    repo_user.add(DMUser(
                  name="TestUser",
                  email="TestUser@email.com",
                  hashed_password=hash_password("TestUserSomePass"),
                  is_company=False,
                  created_at=datetime.utcnow(),
        ))
    # ACT
    request_read = await client_app.get(url="/users")
    # ASSERT
    assert request_read.status_code == 200, "Не удалось получить список пользователей"


@pytest.mark.asyncio
async def test_user_update(client_app, sa_session, current_user):
    """Тест эндпоинта редактирования пользователя"""
    # ARRANGE
    data_to_update = UserUpdateSchema(
        name="updated_name",
        email="updated_user@email.com",
        is_company = True
    )
    # ACT
    request_update_user = await client_app.put(
        "/users",
        params={"id":current_user.id},
        json=data_to_update.dict())
    # ASSERT
    assert request_update_user.status_code == 200, "Ошибка при редактировании пользователя"


@pytest.mark.asyncio
async def test_add_job(client_app, sa_session, current_user):
    """Тест эндпоинта создания job"""
    # ARRANGE
    current_user.name = "hello"
    current_user.is_company = True
    sa_session.add(current_user)
    sa_session.flush()
    await sa_session.commit()

    job_to_add = {
        # user_id:request_add_user.json()["id"],
        "title": "some_a_very_interesting_job",
        "description":"the_job_is_really_very interesting",
        "salary_from": 2.0, #Decimal(2.0),
        "salary_to": 3.0, #Decimal(3.0),
        "is_active": True,
        # created_at:datetime.utcnow(),
    }

    # ACT
    request_add_job = await client_app.post(url="/job", json=job_to_add)
    # ASSERT
    assert request_add_job.status_code == 200, "Ошибка при размещении вакансии"
    assert request_add_job.json()["title"] == "some_a_very_interesting_job", "Ошибка при размещении вакансии"


@pytest.mark.asyncio
async def test_respond_vacancy(client_app, sa_session, current_user, test_job):
    # ARRANGE
    sa_session.add(test_job)
    sa_session.flush()
    await sa_session.commit()

    current_user.is_company = False
    await sa_session.merge(current_user)
    await sa_session.commit()

    job_response = await client_app.patch(
        url=f"/users/{test_job.id}",
        params={"message": "job_response_message",},
    )
    assert job_response.status_code == 200, "Ошибка работы эндпоинта отклика на вакансию"
    assert job_response.json()["message"] == "job_response_message", "Ошибка работы эндпоинта отклика на вакансию"


@pytest.mark.asyncio
async def test_read_vacancies(client_app, sa_session, current_user, test_job):
    # ARRANGE
    sa_session.add(test_job)
    sa_session.flush()
    await sa_session.commit()
    # ACT
    request_jobs = await client_app.get(url="/job/jobs")
    # ASSERT
    assert request_jobs.status_code == 200, "Ошибка в запросе списка доступных вакансий"


@pytest.mark.asyncio
async def test_edit_job(client_app, sa_session, current_user, test_job):
    # ARRANGE
    test_job.user_id = current_user.id
    await sa_session.merge(test_job)
    await sa_session.commit()

    edited_job = {
        "title": "edited_job",
        "description": "edited_description",
        "salary_from": 1.,
        "salary_to": 10.,
        "is_active": True,
    }
    # ACT
    job_edit_response = await client_app.put(url=f"/job/{test_job.id}", json=edited_job)
    # ASSERT
    assert job_edit_response.status_code == 200, "Ошибка при реадктировании вакансии"
    assert job_edit_response.json()["title"] == "edited_job", "Ошибка при реадктировании вакансии"


@pytest.mark.asyncio
async def test_delete_job(client_app, sa_session, current_user, test_job):
    # ARRANGE
    current_user.is_company = True
    await sa_session.merge(current_user)
    test_job.user_id=current_user.id
    await sa_session.merge(test_job)
    await sa_session.commit()
    # ACT
    delete_response = await client_app.delete(url=f"/job/{test_job.id}")
    # ASSERT
    assert delete_response.status_code == 200, "Ошибка при удалении вакансии %" % 0

@pytest.mark.asyncio
async def test_get_responses(client_app, sa_session, current_user, test_job):
    # ARRANGE
    sa_session.add(test_job)
    sa_session.flush()
    await sa_session.commit()
    # Response for the test job
    job_response = models.Response(
        user_id=current_user.id,
        job_id=test_job.id,
        message="I want to do the job",
    )
    sa_session.add(job_response)
    sa_session.flush()
    await sa_session.commit()
    # ACT
    read_job_responses = await client_app.get(url=f"/response/{test_job.id}")
    # ASSERT
    assert read_job_responses.status_code == 200, "Ошибка в запросе откликов на вакансию %s" % 0
    assert read_job_responses.json()[0]["message"] == "I want to do the job", "Ошибка в запросе откликов на вакансию %s" % 0
