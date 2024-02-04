from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Query, Path
from starlette.responses import JSONResponse

from api.schemas.job_schemas import SimpleTextReport
from api.schemas.response_schema import SResponseForJob
from applications.queries.response_query import respond_to_vacancy
from applications.queries.user_queries import update_current_user
from db_settings import DB_HOST, DB_NAME, DB_PASS, DB_USER
from api.schemas.user import UserSchema, UserInSchema, UserUpdateSchema
from applications.dependencies import get_db, get_current_user
from sqlalchemy.ext.asyncio import AsyncSession
from applications.queries import user_queries as user_queries
from infrastructure.repos import RepoUser
from models import User


router = APIRouter(prefix="/users", tags=["users"])


@router.get("", response_model=List[UserSchema])
async def read_users(
    db: AsyncSession = Depends(get_db),
    limit: int = 100,
    skip: int = 0):
    res = await user_queries.get_all(db=db, limit=limit, skip=skip)
    if res.errors:
        return JSONResponse(
            content=str(res.errors),
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    return res.result


@router.post("", response_model=UserSchema)
async def create_user(user: UserInSchema, db: AsyncSession = Depends(get_db)):
    res = await user_queries.create(db=db, user_schema=user)
    if res.errors:
        return JSONResponse(
            content=str(res.errors),
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    return UserSchema.from_orm(res.result)
    # return UserSchema.from_attributes(user)


@router.put("", response_model=UserSchema)
async def update_user(
    id: int,
    user: UserUpdateSchema,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    result = await update_current_user(id, user, db, current_user)

    if result.errors:
        return JSONResponse(
            content=str(result.errors),
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    new_user = result.result
    return UserSchema.from_orm(new_user)

@router.patch("/{job_id}", summary="Откликнуться на вакансию")    # add response model
async def respond_vacancy(
        job_id: int = Path(description="Идентификатор (записи о) вакансии"),
        message: str = Query(description="Текст сопроводительного письма", max_length=2000),
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user),
    ):
    if current_user.is_company:
        msg = "Пользователь %s является компанией-работодателем, поэтому не может откликаться на вакансии" % current_user.name
        return JSONResponse(
            content=msg,
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
        )
    else:
        try:
            job_resp_schema = SResponseForJob(
                job_id=job_id,
                user_id=current_user.id,
                message=message,
            )
            res = await respond_to_vacancy(db, job_resp_schema)
            if res.errors:
                return JSONResponse(
                    content=str(res.errors),
                    status_code=status.HTTP_409_CONFLICT,
                )
            return SimpleTextReport(id=res.result.id, message="Добавлен отклик %s на вакансию %s" % (res.result.id, job_id))
        except Exception as e:
            msg = "Ошибка при создании отклика на вакансию %s; %s" % (job_id, str(e))
            return JSONResponse(
                content=msg,
                status_code=status.HTTP_400_BAD_REQUEST,
            )



@router.get("/get_env", deprecated=True, summary="probe_endpoint")
def get_env():
    response = "|".join((DB_USER, DB_PASS, DB_HOST, DB_NAME))
    return response
