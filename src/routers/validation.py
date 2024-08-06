from typing import List, Union

from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from models import Job, Response, User
from queries import jobs as jobs_queries
from queries import responses as responses_queries
from schemas import ResponsesCreateSchema


class Real_Validation:
    @staticmethod
    def empty_base(elements: Union[User, List[User], None], router_name: str) -> None:
        if not elements:
            return JSONResponse(
                status_code=422,
                content={"message": "{router} is empty".format(router=router_name)},
            )

    @staticmethod
    def element_not_found(elements: Union[User, Job, Response, None], router_name: str) -> None:
        if not elements:
            return JSONResponse(
                status_code=422,
                content={"message": "{router} not found in database".format(router=router_name)},
            )

    @staticmethod
    def is_company_for_job(elem: bool) -> None:
        if not elem:
            return JSONResponse(status_code=422, content={"message": "User is not company"})

    @staticmethod
    def is_company_for_response(elem: bool) -> None:
        if elem:
            return JSONResponse(
                status_code=422,
                content={"message": "Only not company user can read there responses"},
            )

    @staticmethod
    def element_not_current_user_for(
        el1: Union[int], el2: Union[int], router_name: str, action_name: str
    ) -> None:
        if el1 != el2:
            return JSONResponse(
                status_code=403,
                content={
                    "message": "it is not your {router} to {action}".format(
                        router=router_name, action=action_name
                    )
                },
            )

    @staticmethod
    async def post_responses_validation(
        db: AsyncSession, current_user: User, response: ResponsesCreateSchema
    ) -> None:
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
        is_active_job = await jobs_queries.get_by_id(db=db, job_id=response.job_id)
        if not is_active_job:
            return JSONResponse(
                status_code=422,
                content={
                    "message": "{router} not found in database".format(
                        router=f"Job {response.job_id}"
                    )
                },
            )
        if not is_active_job.is_active:
            return JSONResponse(status_code=422, content={"message": "Job is not active"})

    @staticmethod
    async def patch_responses_validation(
        db: AsyncSession, responce_to_patch: Union[ResponsesCreateSchema, None]
    ) -> None:
        if not responce_to_patch:
            return JSONResponse(
                status_code=422,
                content={
                    "message": "it is not your {router} to {action}".format(
                        router="Respose", action="update"
                    )
                },
            )
        is_active_job = await jobs_queries.get_by_id(db=db, job_id=responce_to_patch.job_id)
        if not is_active_job:
            return JSONResponse(
                status_code=422,
                content={
                    "message": "{router} not found in database".format(
                        router=f"Job {responce_to_patch.job_id}"
                    )
                },
            )
        if not is_active_job.is_active:
            return JSONResponse(status_code=422, content={"message": "Job is not active"})
