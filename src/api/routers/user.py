from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Query, Path

from api.schemas.response_schema import SResponseForJob
from applications.queries.response_query import respond_to_vacancy
from db_settings import DB_HOST, DB_NAME, DB_PASS, DB_USER
from api.schemas.user import UserSchema, UserInSchema, UserUpdateSchema
from applications.dependencies import get_db, get_current_user
from sqlalchemy.ext.asyncio import AsyncSession
from applications.queries import user_queries as user_queries
from models import User


router = APIRouter(prefix="/users", tags=["users"])


@router.get("", response_model=List[UserSchema])
async def read_users(
    db: AsyncSession = Depends(get_db),
    limit: int = 100,
    skip: int = 0):
    return await user_queries.get_all(db=db, limit=limit, skip=skip)


@router.post("", response_model=UserSchema)
async def create_user(user: UserInSchema, db: AsyncSession = Depends(get_db)):
    user = await user_queries.create(db=db, user_schema=user)
    return UserSchema.from_orm(user)
    # return UserSchema.from_attributes(user)


@router.put("", response_model=UserSchema)
async def update_user(
    id: int,
    user: UserUpdateSchema,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    old_user = await user_queries.get_by_id(db=db, id=id)

    if old_user is None or old_user.email != current_user.email:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь не найден")

    old_user.name = user.name if user.name is not None else old_user.name
    old_user.email = user.email if user.email is not None else old_user.email
    old_user.is_company = user.is_company if user.is_company is not None else old_user.is_company

    new_user = await user_queries.update(db=db, user=old_user)

    # return UserSchema.from_orm(new_user)
    return UserSchema.from_attributes(new_user)

@router.patch("/{job_id}", summary="Откликнуться на вакансию")    # add response model
async def response_vacancy(
        job_id: int = Path(description="Идентификатор (записи о) вакансии"),
        message: str = Query(description="Текст сопроводительного письма", max_length=2000),
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user),
    ):
    if current_user.is_company:
        msg = "Пользователь %s является компанией-работодателем, поэтому не может откликаться на вакансии" % current_user.name
        raise HTTPException(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
            detail=msg,
        )
    else:
        try:
            job_resp_schema = SResponseForJob(
                job_id=job_id,
                user_id=current_user.id,
                message=message,
            )
            await respond_to_vacancy(db, job_resp_schema)
        except Exception as e:
            msg = "Ошибка при создании отклика на вакансию %s" % (job_id)
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=msg,
            )



@router.get("/get_env", deprecated=True, summary="probe_endpoint")
def get_env():
    response = "|".join((DB_USER, DB_PASS, DB_HOST, DB_NAME))
    return response