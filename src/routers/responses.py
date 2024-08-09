"""" Model Responses API  """

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import get_current_user, get_db
from models import User
from queries import jobs as jobs_queries
from queries import responses as responses_queries
from schemas import ResponsesCreateSchema, ResponsesSchema, ResponsesUpdateSchema

from .validation import Real_Validation

router = APIRouter(prefix="/responses", tags=["responses"])
responses = {
    204: {"description": "Zero rezult"},
    403: {"description": "You have not power here"},
    422: {"description": "Some proplem with validation"},
}
responses_get = {
    **responses,
    200: {
        "description": "Get response\\es",
        "content": {
            "application/json": {
                "example": {
                    "id": 1,
                    "user_id": 1,
                    "job_id": 1,
                    "message": "dreem work",
                    "created_at": "2024-08-06T20:41:48.521Z",
                }
            }
        },
    },
}

responses_post = {
    **responses,
    200: {
        "description": "response create",
        "content": {
            "application/json": {
                "example": {
                    "message": "response create",
                    "new responce messege": "dreem_WoRk",
                    "created_at": "2024-08-06T20:41:48.521Z",
                }
            }
        },
    },
}

responses_update = {
    **responses,
    200: {
        "description": "response updated",
        "content": {
            "application/json": {
                "example": {
                    "message": "response update",
                    "new responce messege": "super_work",
                }
            }
        },
    },
}
responses_delete = {
    **responses,
    200: {
        "description": "response delete",
        "content": {
            "application/json": {
                "example": {
                    "message": "Response delete",
                    "Response id": 5,
                    "job_id": 1,
                    "Response message": "Great_work",
                }
            }
        },
    },
}


@router.get(
    "/responses_job_id/{job_id}", response_model=list[ResponsesSchema], responses={**responses_get}
)
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
    looking_job = await jobs_queries.get_by_id(db=db, job_id=job_id)
    Real_Validation.element_not_found(looking_job)
    if not current_user.is_company:
        responses_of_job_id = [
            await responses_queries.get_response_by_job_id_and_user_id(
                db=db, job_id=job_id, user_id=current_user.id
            )
        ]
    elif looking_job.user_id == current_user.id:
        responses_of_job_id = await responses_queries.get_response_by_job_id(db=db, job_id=job_id)
    else:
        Real_Validation.element_not_current_user_for(1, 0, "Respose", "read")

    Real_Validation.element_not_found(responses_of_job_id)
    return responses_of_job_id


@router.get("/responses_user", response_model=list[ResponsesSchema], responses={**responses_get})
async def get_responses_by_user(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Get responses by user id:
    db: datebase connection;
    current_user: current user
    """
    Real_Validation.is_company_for_response(current_user.is_company)
    responses_of_user = await responses_queries.get_response_by_user_id(
        db=db, user_id=current_user.id
    )
    Real_Validation.element_not_found(responses_of_user)
    return responses_of_user


@router.post(
    "/post_response/{job_id}", response_model=ResponsesCreateSchema, responses={**responses_post}
)
async def create_response(
    job_id: int,
    response: ResponsesCreateSchema,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Create response:
    job_id id of job, where we want create response
    response: dataset for ResponsesCreateSchema
    db: datebase connection;
    current_user: current user
    """
    Real_Validation.is_company_for_response(current_user.is_company)
    await Real_Validation.post_responses_validation(db, current_user, job_id)
    new_response = await responses_queries.response_create(
        db=db, response_schema=response, user_id=current_user.id, job_id=job_id
    )
    return JSONResponse(
        status_code=201,
        content={
            "message": "response create",
            "new responce messege": new_response.message,
            "created at": str(new_response.created_at),
        },
    )


@router.patch(
    "/patch_response/{job_id}", response_model=ResponsesSchema, responses={**responses_update}
)
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
    Real_Validation.is_company_for_response(current_user.is_company)
    responce_to_patch = await responses_queries.get_response_by_job_id_and_user_id(
        db=db, job_id=job_id, user_id=current_user.id
    )
    await Real_Validation.patch_responses_validation(db, responce_to_patch)
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


@router.delete("/delete_response/job/{job_id}", responses={**responses_delete})
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
    Real_Validation.is_company_for_response(current_user.is_company)
    respose_to_delete = await responses_queries.get_response_by_job_id_and_user_id(
        db=db, job_id=job_id, user_id=current_user.id
    )
    Real_Validation.element_not_found(respose_to_delete)
    delete_responses = await responses_queries.delete(db=db, response=respose_to_delete)
    return JSONResponse(
        status_code=200,
        content={
            "message": "Response delete",
            "Response id": delete_responses.id,
            "job_id": delete_responses.job_id,
            "Response message": delete_responses.message,
        },
    )


@router.delete("/delete_response/{response_id}", responses={**responses_delete})
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
    Real_Validation.is_company_for_response(current_user.is_company)
    responce_to_delete = await responses_queries.get_response_by_id(db=db, response_id=response_id)
    Real_Validation.element_not_found(responce_to_delete)
    Real_Validation.element_not_current_user_for(
        responce_to_delete.user_id, current_user.id, router_name="response", action_name="delete"
    )
    respose_to_delete = await responses_queries.delete(db=db, response=responce_to_delete)
    return JSONResponse(
        status_code=200,
        content={
            "message": "Response delete",
            "Response id": respose_to_delete.id,
            "job_id": respose_to_delete.job_id,
            "Response message": respose_to_delete.message,
        },
    )
