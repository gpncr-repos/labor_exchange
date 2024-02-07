from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Query, Path

from api.schemas.response_schema import SResponseForJob
from applications.queries.user_queries import update_current_user, respond_to_vacancy
from db_settings import DB_HOST, DB_NAME, DB_PASS, DB_USER
from api.schemas.user import UserSchema, UserInSchema, UserUpdateSchema
from applications.dependencies import get_db, get_current_user
from sqlalchemy.ext.asyncio import AsyncSession
from domain.do_schemas import DOUser, DOResponse
from infrastructure.repos import RepoUser
from models import User

router = APIRouter(prefix="/users", tags=["users"])


@router.get("", response_model=List[UserSchema])
async def read_users(
        db: AsyncSession = Depends(get_db),
        limit: int = 100,
        skip: int = 0):
    """Возвращает список пользователей"""
    repo_user = RepoUser(db)
    orm_objs = await repo_user.get_all(limit, skip)
    users = [UserSchema.from_orm(orm_obj) for orm_obj in orm_objs]
    return users


@router.post("", response_model=UserSchema)
async def create_user(
        user_schema: UserInSchema,
        db: AsyncSession = Depends(get_db),
):
    #
    # user = User(
    #     name=user_schema.name,
    #     email=user_schema.email,
    #     hashed_password=hash_password(user_schema.password),
    #     is_company=user_schema.is_company,
    #     # created_at=datetime.utcnow(),
    # )
    repo_user = RepoUser(db)
    user_orm = await repo_user.add(user_schema)
    user_s = UserSchema.from_orm(user_orm)
    return user_s


@router.put("", response_model=UserSchema)
async def update_user(
        id: int,
        user: UserUpdateSchema,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user),
):
    user_do = DOUser(
        name=user.name,
        email=user.email,
        is_company=user.is_company,
    )
    updated_user = await update_current_user(id, user_do, db, current_user.email)
    return UserSchema.from_orm(updated_user)


@router.patch("/{job_id}", summary="Откликнуться на вакансию")  # add response model
async def respond_vacancy(
        job_id: int = Path(description="Идентификатор (записи о) вакансии"),
        message: str = Query(description="Текст сопроводительного письма", max_length=2000),
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user),
):
    if current_user.is_company:
        msg = "Пользователь %s является компанией-работодателем, поэтому не может откликаться на вакансии" % current_user.name
        raise HTTPException(
            detail=msg,
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
        )
    else:
        try:
            job_resp_schema = DOResponse(
                job_id=job_id,
                user_id=current_user.id,
                message=message,
            )
            res = await respond_to_vacancy(db, job_resp_schema)
            return SResponseForJob.from_orm(res)
        except Exception as e:
            msg = "Ошибка при создании отклика на вакансию %s; %s" % (job_id, str(e))
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=msg,
            )


@router.get("/get_env", deprecated=True, summary="probe_endpoint")
def get_env():
    response = "|".join((DB_USER, DB_PASS, DB_HOST, DB_NAME))
    return response
