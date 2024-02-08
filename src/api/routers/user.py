from datetime import datetime
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Query, Path

from api.schemas.response_schema import SResponseForJob
from applications.queries.user_queries import update_current_user, respond_to_vacancy
from core.security import hash_password
from db_settings import DB_HOST, DB_NAME, DB_PASS, DB_USER
from api.schemas.user import UserSchema, UserInSchema, UserUpdateSchema
from applications.dependencies import get_db, get_current_user
from sqlalchemy.ext.asyncio import AsyncSession
from domain.dm_schemas import DMUser, DMResponse
from infrastructure.repos import RepoUser
from models import User

router = APIRouter(prefix="/users", tags=["users"])


@router.post(
    "",
    response_model=UserSchema,
    summary="Создание пользователя",
)
async def create_user(
        user_schema: UserInSchema,
        db: AsyncSession = Depends(get_db),
):
    """
    Добавляет пользователя: запись в таблицу users с переданными параметрами

    :param user_schema: UserInSchema объект с параметрами создаваемого пользователя
    :param db: AsyncSession объект сессия для работы с базой данных
    :returns: пары поле:значение добавленной записи
    :rtype: UserSchema
    """
    user_dm = DMUser(
        name=user_schema.name,
        email=user_schema.email,
        hashed_password=hash_password(user_schema.password),
        is_company=user_schema.is_company,
        created_at=datetime.utcnow(),
    )
    repo_user = RepoUser(db)
    user_new = await repo_user.add(user_dm)
    user_s = UserSchema.from_orm(user_new)
    return user_s


@router.get(
    "",
    response_model=List[UserSchema],
    summary="Получение списка пользователей"
)
async def read_users(
        db: AsyncSession = Depends(get_db),
        limit: int = 100,
        skip: int = 0,
):
    """
    Возвращает не более limit пользователей из таблицы users, начиная с skip'й записи

    :param db: AsyncSession объект сессия для работы с базой данных
    :param limit: int количество запрашиваемых записей
    :param skip: запись, с которой следует начать выборку
    """
    repo_user = RepoUser(db)
    users_dm = await repo_user.get_all(limit, skip)
    users = [UserSchema.from_orm(user_dm) for user_dm in users_dm]
    return users


@router.put(
    "",
    response_model=UserSchema,
    summary="Редактирование данных пользователя"
)
async def update_user(
        id: int,
        user: UserUpdateSchema,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user),
):
    """Заменяет параметры пользователя на переданные по запросу пользователя

    :param id: int идентификатор вакансии
    :param user: UserUpdateSchema объект с новыми параметрами
    :param db: AsyncSession объект сессия для работы с базой данных
    :param current_user: User объект пользователь
    :returns: пары поле:значение добавленной записи
    :rtype: UserSchema
    """
    user_dm = DMUser(
        name=user.name,
        email=user.email,
        is_company=user.is_company,
    )
    updated_user = await update_current_user(id, user_dm, db, current_user.email)
    return UserSchema.from_orm(updated_user)


@router.patch(
    "/{job_id}",
    summary="Откликнуться на вакансию",
    response_model=SResponseForJob,
)
async def respond_vacancy(
        job_id: int = Path(description="Идентификатор (записи о) вакансии"),
        message: str = Query(description="Текст сопроводительного письма", max_length=2000),
        db: AsyncSession = Depends(get_db),
        current_user: DMUser = Depends(get_current_user),
):
    """
    Добавляет запись в таблицу responses - отклик пользователя на вакансию

    :param job_id: int идентификатор вакансии
    :param message: str текст сопроводительного письма
    :param db: AsyncSession объект сессия для работы с базой данных
    :param current_user: User объект пользователь, откликающийся на вакансию
    :returns: пары поле:значение добавленной записи
    :rtype: SResponseForJob
    """
    if current_user.is_company:
        msg = "Пользователь %s является компанией-работодателем, поэтому не может откликаться на вакансии" % current_user.name
        raise HTTPException(
            detail=msg,
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
        )
    else:
        try:
            job_resp_schema = DMResponse(
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
