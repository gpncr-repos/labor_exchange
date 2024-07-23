from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from schemas import UserSchema, UserInSchema, UserUpdateSchema,UserGetSchema
from dependencies import get_db, get_current_user
from sqlalchemy.ext.asyncio import AsyncSession
from queries import user as user_queries
from models import User


router = APIRouter(prefix="/users", tags=["users"])


@router.get("", response_model=List[UserGetSchema])
async def read_users(
    db: AsyncSession = Depends(get_db),
    limit: int = 100,
    skip: int = 0):
    """
    Выдача пользователей по limit штук от skip:
    db: коннект к базе данных
    limit: кол-во записей для вывода,
    skip: от какой записи начинать вывод):
    """
    res=await user_queries.get_all(db=db, limit=limit, skip=skip)
    if len(res)==0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="В базе данных нет пользователей")
    return res

@router.get("/{user_id}", response_model=UserSchema)
async def read_users(
    user_id: int,
    db: AsyncSession = Depends(get_db)
    ):
    """
    Выдача пользователя по ID:
    user_id: ID пользователя
    db: коннект к базе данных
    """
    res=await user_queries.get_by_id(db=db, id=user_id)
    if res is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь не найден")
    return res

@router.post("", response_model=UserSchema)
async def create_user(user: UserInSchema, db: AsyncSession = Depends(get_db)):
    """
    Создание пользователя:
    user: данные для создания пользователя согласно схемы UserInSchema
    db: коннект к базе данных
    """
    res = await user_queries.create(db=db, user_schema=user)
    return UserSchema.from_orm(res)


@router.put("", response_model=UserUpdateSchema)
async def update_user(
    id: int,
    user: UserUpdateSchema,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)):
    """
    Обновление пользователя:
    id: ID пользователя, которого будем исправлять
    user: данные для создания пользователя согласно схемы UserUpdateSchema
    db: коннект к базе данных
    current_user: проверка существующего юзера
    """
    old_user = await user_queries.get_by_id(db=db, id=id)

    if old_user is None or old_user.email != current_user.email:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь не найден")

    old_user.name = user.name if user.name is not None else old_user.name
    old_user.email = user.email if user.email is not None else old_user.email
    old_user.is_company = user.is_company if user.is_company is not None else old_user.is_company

    new_user = await user_queries.update(db=db, user=old_user)

    return UserUpdateSchema.from_orm(new_user)
