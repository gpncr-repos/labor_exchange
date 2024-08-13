"""" Model Responses API  """

from fastapi import APIRouter, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import get_current_user, get_db
from models import User
from queries import jobs as jobs_queries
from queries import responses as responses_queries
from schemas import ResponsesCreateSchema, ResponsesSchema, ResponsesUpdateSchema

from .response_examples.responses import (
    responses_delete_responses,
    responses_get_responses,
    responses_post_responses,
    responses_update_responses,
)
from .validation import Real_Validation

router = APIRouter(prefix="/responses", tags=["responses"])


@router.get(
    "/{job_id}", response_model=list[ResponsesSchema], responses={**responses_get_responses}
)
async def get_responses_by_job_id(
    job_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Get responses by job id:\n
    job_id: job id\n
    db: datebase connection;\n
    current_user: current user\n
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
        Real_Validation.element_not_current_user_for(1, 0, "Job", "read")
    Real_Validation.element_not_found(responses_of_job_id[0])
    list_of_responses = []
    for response in responses_of_job_id:
        list_of_responses.append(ResponsesSchema(**response.__dict__))
    return list_of_responses


@router.get("", response_model=list[ResponsesSchema], responses={**responses_get_responses})
async def get_responses_by_user(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Get responses by user id:\n
    db: datebase connection;\n
    current_user: current user\n
    """
    Real_Validation.is_company_for_response(current_user.is_company)
    responses_of_user = await responses_queries.get_response_by_user_id(
        db=db, user_id=current_user.id
    )
    Real_Validation.element_not_found(responses_of_user)
    list_of_responses = []
    for response in responses_of_user:
        list_of_responses.append(ResponsesSchema(**response.__dict__))
    return list_of_responses


@router.post("", response_model=ResponsesSchema, responses={**responses_post_responses})
async def create_response(
    response_for_status: Response,
    response: ResponsesCreateSchema,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Create response:\n
    job_id id of job, where we want create response\n
    response: dataset for ResponsesCreateSchema\n
    db: datebase connection;\n
    current_user: current user\n
    """
    Real_Validation.is_company_for_response(current_user.is_company)
    await Real_Validation.post_responses_validation(db, current_user, response.job_id)
    new_response = await responses_queries.response_create(
        db=db, response_schema=response, user_id=current_user.id, job_id=response.job_id
    )
    response_for_status.status_code = 201
    return ResponsesSchema(**new_response.__dict__)


@router.patch("", response_model=ResponsesSchema, responses={**responses_update_responses})
async def patch_response(
    response: ResponsesUpdateSchema,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Patch response:\n
    job_id: job id\n
    response: dataset for ResponsesCreateSchema\n
    db: datebase connection;\n
    current_user: current user\n
    """
    Real_Validation.is_company_for_response(current_user.is_company)
    responce_to_patch = await responses_queries.get_response_by_id(db=db, response_id=response.id)
    await Real_Validation.patch_responses_validation(db, responce_to_patch)
    responce_to_patch.message = (
        response.message if response.message is not None else responce_to_patch.message
    )
    new_response = await responses_queries.update(db=db, response=responce_to_patch)
    return ResponsesSchema(**new_response.__dict__)


@router.delete("/jobs/{job_id}", responses={**responses_delete_responses})
async def delete_response(
    job_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    delete responses by job_id:\n
    job_id: job id\n
    db: datebase connection;\n
    current_user: current user\n
    """
    Real_Validation.is_company_for_response(current_user.is_company)
    respose_to_delete = await responses_queries.get_response_by_job_id_and_user_id(
        db=db, job_id=job_id, user_id=current_user.id
    )
    Real_Validation.element_not_found(respose_to_delete)
    delete_responses = await responses_queries.delete(db=db, response=respose_to_delete)
    return ResponsesSchema(**delete_responses.__dict__)


@router.delete("/{response_id}", responses={**responses_delete_responses})
async def delete_response_by_id(
    response_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    delete responses by id:\n
    id: response id\n
    db: datebase connection;\n
    current_user: current user\n
    """
    Real_Validation.is_company_for_response(current_user.is_company)
    responce_to_delete = await responses_queries.get_response_by_id(db=db, response_id=response_id)
    Real_Validation.element_not_found(responce_to_delete)
    Real_Validation.element_not_current_user_for(
        responce_to_delete.user_id, current_user.id, router_name="response", action_name="delete"
    )
    respose_to_delete = await responses_queries.delete(db=db, response=responce_to_delete)
    return ResponsesSchema(**respose_to_delete.__dict__)
