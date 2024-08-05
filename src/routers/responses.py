"""" Model Responses API  """

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import get_current_user, get_db
from models import User
from queries import jobs as jobs_queries
from queries import responses as responses_queries
from schemas import ResponsesCreateSchema, ResponsesSchema, ResponsesUpdateSchema

from .validation import Validation_for_routers

router = APIRouter(prefix="/responses", tags=["responses"])


@router.get("/responses_job_id/{job_id}", response_model=list[ResponsesSchema])
async def get_responses_by_job_id(
    job_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Get responses by job id:
    job_id: job id
    db: datebase connection;
    current_user: current user
    """
    looking_job = await jobs_queries.get_by_id(db=db, id=job_id)
    if not current_user.is_company:
        responses_of_job_id = [
            await responses_queries.get_response_by_job_id_and_user_id(
                db=db, job_id=job_id, user_id=current_user.id
            )
        ]
    elif looking_job.user_id == current_user.id:
        responses_of_job_id = await responses_queries.get_response_by_job_id(db=db, job_id=job_id)
    else:
        return Validation_for_routers.element_not_current_user_for("Respose", "read")
    if not responses_of_job_id:
        return Validation_for_routers.element_not_found("Responses")
    return responses_of_job_id


@router.get("/responses_user/", response_model=list[ResponsesSchema])
async def get_responses_by_user(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Get responses by user id:
    db: datebase connection;
    current_user: current user
    """
    if not current_user.is_company:
        return JSONResponse(
            status_code=422,
            content={"message": "Only not company user can read there responses"},
        )
    responses_of_user = await responses_queries.get_response_by_user_id(
        db=db, user_id=current_user.id
    )
    if not responses_of_user:
        return Validation_for_routers.element_not_current_user_for("Respose", "read")
    return responses_of_user


@router.post("", response_model=ResponsesCreateSchema)
async def create_response(
    response: ResponsesCreateSchema,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Create response:
    response: dataset for ResponsesCreateSchema
    db: datebase connection;
    current_user: current user
    """
    if current_user.is_company:
        return JSONResponse(
            status_code=422,
            content={"message": "Companies are prohibited from creating responses"},
        )
    is_double_responce = await responses_queries.get_response_by_job_id_and_user_id(
        db=db, job_id=response.job_id, user_id=current_user.id
    )
    if is_double_responce:
        return JSONResponse(
            status_code=422,
            content={"message": "You alredy have response for thise job"},
        )
    is_active_job = await jobs_queries.get_by_id(db=db, id=response.job_id)
    if not is_active_job:
        return Validation_for_routers.element_not_found(f"Job {response.job_id}")
    if not is_active_job.is_active:
        return Validation_for_routers.job_is_not_active()
    new_response = await responses_queries.response_create(
        db=db, response_schema=response, user_id=current_user.id
    )
    return JSONResponse(
        status_code=201,
        content={
            "message": "response create",
            "new responce messege": new_response.message,
        },
    )


@router.patch("/patch_response/{job_id}", response_model=ResponsesSchema)
async def patch_response(
    job_id: int,
    response: ResponsesUpdateSchema,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Patch response:
    job_id: job id
    response: dataset for ResponsesCreateSchema
    db: datebase connection;
    current_user: current user
    """
    responce_to_patch = await responses_queries.get_response_by_job_id_and_user_id(
        db=db, job_id=job_id, user_id=current_user.id
    )
    if not responce_to_patch:
        return Validation_for_routers.element_not_current_user_for("Respose", "update")
    is_active_job = await jobs_queries.get_by_id(db=db, id=response.job_id)
    if not is_active_job:
        return Validation_for_routers.element_not_found(f"Job {job_id}")
    if not is_active_job.is_active:
        return Validation_for_routers.job_is_not_active()
    responce_to_patch.message = (
        response.message if response.message is not None else responce_to_patch.message
    )
    new_response = await responses_queries.update(db=db, response=responce_to_patch)
    return JSONResponse(
        status_code=201,
        content={
            "message": "response update",
            "new responce messege": new_response.message,
        },
    )


@router.delete("/delete_response/job/{job_id}")
async def delete_response(
    job_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    delete responses by job_id:
    job_id: job id
    db: datebase connection;
    current_user: current user
    """
    respose_to_delete = await responses_queries.get_response_by_job_id_and_user_id(
        db=db, job_id=job_id, user_id=current_user.id
    )
    if not respose_to_delete:
        return Validation_for_routers.element_not_current_user_for("Resposes", "delete")
    delete_responses = await responses_queries.delete(db=db, response=respose_to_delete)
    return JSONResponse(
        status_code=200,
        content={
            "message": "Response delete",
            "job_id": delete_responses.job_id,
        },
    )


@router.delete("/delete_response/{response_id}")
async def delete_response_by_id(
    response_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    delete responses by id:
    id: response id
    db: datebase connection;
    current_user: current user
    """
    responce_to_delete = await responses_queries.get_response_by_id(db=db, response_id=response_id)
    if not responce_to_delete:
        return Validation_for_routers.element_not_found("Responses")
    if responce_to_delete.user_id != current_user.id:
        return Validation_for_routers.element_not_current_user_for("Respose", "delete")
    respose_to_delete = await responses_queries.delete(db=db, response=responce_to_delete)
    return JSONResponse(
        status_code=200,
        content={
            "message": "Response delete",
            "Response id": respose_to_delete.id,
            "Response message": respose_to_delete.message,
        },
    )
