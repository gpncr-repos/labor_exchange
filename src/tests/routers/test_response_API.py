import pytest

from fixtures.responses import ResponseCreateFactory
from tests.create_obj import Conveyor


@pytest.mark.asyncio
async def test_read_response_by_id(client_app, current_user, sa_session):
    current_user = await Conveyor.current_to_company(sa_session, current_user)
    job = await Conveyor.create_job(sa_session, current_user)
    count_workers = 10
    list_of_workers = []
    for _ in range(count_workers):
        user = await Conveyor.create_woker(sa_session)
        response = await Conveyor.create_response(sa_session, user, job)
        list_of_workers.append(user)
    response = await client_app.get(f"/responses/{job.id}")
    assert response.status_code == 200
    assert len(response.json()) == count_workers
    response = await client_app.get("/responses/-1")
    assert response.status_code == 204


@pytest.mark.asyncio
async def test_read_all_user_responses(client_app, current_user, sa_session):
    emploer = await Conveyor.create_emploer(sa_session)
    current_user = await Conveyor.current_to_worker(sa_session, current_user)
    count_responses = 10
    for _ in range(count_responses):
        job = await Conveyor.create_job(sa_session, emploer)
        response = await Conveyor.create_response(sa_session, current_user, job)
    response = await client_app.get("/responses")
    assert response.status_code == 200
    assert len(response.json()) == count_responses


@pytest.mark.asyncio
async def test_read_all_user_company_responses(client_app, current_user, sa_session):
    emploer = await Conveyor.create_emploer(sa_session)
    current_user = await Conveyor.current_to_worker(sa_session, current_user)
    count_responses = 10
    for _ in range(count_responses):
        job = await Conveyor.create_job(sa_session, emploer)
        response = await Conveyor.create_response(sa_session, current_user, job)
    current_user = await Conveyor.current_to_company(sa_session, current_user)
    response = await client_app.get("/responses")
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_read_all_user_responses_empty(client_app, current_user, sa_session):
    current_user = await Conveyor.current_to_worker(sa_session, current_user)
    response = await client_app.get("/responses")
    assert response.status_code == 204


@pytest.mark.asyncio
async def test_post_response_norm(client_app, current_user, sa_session):
    emploer = await Conveyor.create_emploer(sa_session)
    job = await Conveyor.create_job(sa_session, emploer)
    current_user = await Conveyor.current_to_worker(sa_session, current_user)
    response_massage = (ResponseCreateFactory.stub()).__dict__
    response_massage["job_id"] = job.id
    response = await client_app.post("/responses", json=response_massage)
    assert response.status_code == 201


@pytest.mark.asyncio
async def test_post_response_company(client_app, current_user, sa_session):
    emploer = await Conveyor.create_emploer(sa_session)
    job = await Conveyor.create_job(sa_session, emploer)
    current_user = await Conveyor.current_to_company(sa_session, current_user)
    response_massage = (ResponseCreateFactory.stub()).__dict__
    response_massage["job_id"] = job.id
    response = await client_app.post("/responses", json=response_massage)
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_post_response_job_is_not_active(client_app, current_user, sa_session):
    emploer = await Conveyor.create_emploer(sa_session)
    job = await Conveyor.create_job(sa_session, emploer)
    current_user = await Conveyor.current_to_worker(sa_session, current_user)
    job = await Conveyor.job_to_not_active(sa_session, job)
    response_massage = (ResponseCreateFactory.stub()).__dict__
    response_massage["job_id"] = job.id
    response = await client_app.post("/responses", json=response_massage)
    assert response.status_code == 499


@pytest.mark.asyncio
async def test_post_response_double_response(client_app, current_user, sa_session):
    emploer = await Conveyor.create_emploer(sa_session)
    job = await Conveyor.create_job(sa_session, emploer)
    current_user = await Conveyor.current_to_worker(sa_session, current_user)
    response = await Conveyor.create_response(sa_session, current_user, job)
    response_massage = (ResponseCreateFactory.stub()).__dict__
    response_massage["job_id"] = job.id
    response = await client_app.post("/responses", json=response_massage)
    assert response.status_code == 498


@pytest.mark.asyncio
async def test_post_response_empty_job(client_app, current_user, sa_session):
    emploer = await Conveyor.create_emploer(sa_session)
    job = await Conveyor.create_job(sa_session, emploer)
    current_user = await Conveyor.current_to_worker(sa_session, current_user)
    response_massage = (ResponseCreateFactory.stub()).__dict__
    response_massage["job_id"] = job.id + 1
    response = await client_app.post("/responses", json=response_massage)
    assert response.status_code == 204


@pytest.mark.asyncio
async def test_patch_response_norm(client_app, current_user, sa_session):
    emploer = await Conveyor.create_emploer(sa_session)
    job = await Conveyor.create_job(sa_session, emploer)
    current_user = await Conveyor.current_to_worker(sa_session, current_user)
    response = await Conveyor.create_response(sa_session, current_user, job)
    response_update = await client_app.patch(
        "/responses",
        json={
            "id": response.id,
            "message": response.message + "_update",
        },
    )
    assert response_update.status_code == 200


@pytest.mark.asyncio
async def test_patch_response_company_try(client_app, current_user, sa_session):
    emploer = await Conveyor.create_emploer(sa_session)
    job = await Conveyor.create_job(sa_session, emploer)
    current_user = await Conveyor.current_to_worker(sa_session, current_user)
    response = await Conveyor.create_response(sa_session, current_user, job)
    current_user = await Conveyor.current_to_company(sa_session, current_user)
    response_update = await client_app.patch(
        "/responses",
        json={
            "id": response.id,
            "message": response.message + "_update",
        },
    )
    assert response_update.status_code == 403


@pytest.mark.asyncio
async def test_patch_response_not_exist_response(client_app, current_user, sa_session):
    current_user = await Conveyor.current_to_worker(sa_session, current_user)

    response_update = await client_app.patch(
        "/responses",
        json={
            "id": 1,
            "message": "responde_update",
        },
    )
    assert response_update.status_code == 422


@pytest.mark.asyncio
async def test_patch_response_not_active_job(client_app, current_user, sa_session):
    emploer = await Conveyor.create_emploer(sa_session)
    job = await Conveyor.create_job(sa_session, emploer)
    current_user = await Conveyor.current_to_worker(sa_session, current_user)
    response = await Conveyor.create_response(sa_session, current_user, job)
    job = await Conveyor.job_to_not_active(sa_session, job)
    response_update = await client_app.patch(
        "/responses",
        json={
            "id": response.id,
            "message": response.message + "_update",
        },
    )
    assert response_update.status_code == 499


@pytest.mark.asyncio
async def test_patch_response_not_yours_response(client_app, current_user, sa_session):
    emploer = await Conveyor.create_emploer(sa_session)
    job = await Conveyor.create_job(sa_session, emploer)
    worker = await Conveyor.create_woker(sa_session)
    current_user = await Conveyor.current_to_worker(sa_session, current_user)
    response1 = await Conveyor.create_response(sa_session, worker, job)
    response_update = await client_app.patch(
        "/responses",
        json={
            "id": response1.id,
            "message": response1.message + "_update",
        },
    )
    assert response_update.status_code == 403


@pytest.mark.asyncio
async def test_delete_response_job_id_norm(client_app, current_user, sa_session):
    emploer = await Conveyor.create_emploer(sa_session)
    job = await Conveyor.create_job(sa_session, emploer)
    current_user = await Conveyor.current_to_worker(sa_session, current_user)
    await Conveyor.create_response(sa_session, current_user, job)
    response_update = await client_app.delete(f"/responses/jobs/{job.id}")
    assert response_update.status_code == 200


@pytest.mark.asyncio
async def test_delete_response_job_id_by_company(client_app, current_user, sa_session):
    emploer = await Conveyor.create_emploer(sa_session)
    job = await Conveyor.create_job(sa_session, emploer)
    current_user = await Conveyor.current_to_worker(sa_session, current_user)
    await Conveyor.create_response(sa_session, current_user, job)
    current_user = await Conveyor.current_to_company(sa_session, current_user)
    response_update = await client_app.delete(f"/responses/jobs/{job.id}")
    assert response_update.status_code == 403


@pytest.mark.asyncio
async def test_delete_response_job_id_by_no_response(client_app, current_user, sa_session):
    emploer = await Conveyor.create_emploer(sa_session)
    job = await Conveyor.create_job(sa_session, emploer)
    current_user = await Conveyor.current_to_worker(sa_session, current_user)
    response_update = await client_app.delete(f"/responses/jobs/{job.id}")
    assert response_update.status_code == 204


@pytest.mark.asyncio
async def test_delete_response_id_norm(client_app, current_user, sa_session):
    emploer = await Conveyor.create_emploer(sa_session)
    job = await Conveyor.create_job(sa_session, emploer)
    current_user = await Conveyor.current_to_worker(sa_session, current_user)
    response = await Conveyor.create_response(sa_session, current_user, job)
    response_update = await client_app.delete(f"/responses/{response.id}")
    assert response_update.status_code == 200


@pytest.mark.asyncio
async def test_delete_response_id_by_company(client_app, current_user, sa_session):
    emploer = await Conveyor.create_emploer(sa_session)
    job = await Conveyor.create_job(sa_session, emploer)
    current_user = await Conveyor.current_to_worker(sa_session, current_user)
    response = await Conveyor.create_response(sa_session, current_user, job)
    current_user = await Conveyor.current_to_company(sa_session, current_user)
    response_update = await client_app.delete(f"/responses/{response.id}")
    assert response_update.status_code == 403


@pytest.mark.asyncio
async def test_delete_response_id_empty(client_app, current_user, sa_session):
    current_user = await Conveyor.current_to_worker(sa_session, current_user)
    response_update = await client_app.delete("/responses/20")
    assert response_update.status_code == 204


@pytest.mark.asyncio
async def test_delete_response_id_not_my(client_app, current_user, sa_session):
    current_user = await Conveyor.current_to_company(sa_session, current_user)
    job = await Conveyor.create_job(sa_session, current_user)
    worker = await Conveyor.create_woker(sa_session)
    response = await Conveyor.create_response(sa_session, worker, job)
    response_update = await client_app.delete(f"/responses/{response.id}")
    assert response_update.status_code == 403
