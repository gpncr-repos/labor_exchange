"""" Model Users API  """

from typing import List

from fastapi import APIRouter, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import get_current_user, get_db
from models import User
from queries import user as user_queries
from schemas import UserCreateSchema, UserGetSchema, UserUpdateSchema

from .response_examples.user import (
    responses_delete_user,
    responses_get_user,
    responses_post_user,
    responses_update_user,
)
from .validation import Real_Validation

router = APIRouter(prefix="/users", tags=["users"])


@router.get("", response_model=List[UserGetSchema], responses={**responses_get_user})
async def read_all_users(db: AsyncSession = Depends(get_db), limit: int = 100, skip: int = 0):
    """
    Get limit users skip some:\n
    db: datebase connection;\n
    limit: count of get users,\n
    skip: skip from:\n
    """
    all_users = await user_queries.get_all(db=db, limit=limit, skip=skip)
    Real_Validation.element_not_found(all_users)
    list_of_users = []
    for user in all_users:
        list_of_users.append(UserGetSchema(**user.__dict__))
    return list_of_users


@router.get("/{user_id}", response_model=UserGetSchema, responses={**responses_get_user})
async def read_users(user_id: int, db: AsyncSession = Depends(get_db)):
    """
    Get user by id:\n
    user_id: user id\n
    db: datebase connection;\n
    """
    user_by_id = await user_queries.get_by_id(db=db, user_id=user_id)
    Real_Validation.element_not_found(user_by_id)
    return UserGetSchema(**user_by_id.__dict__)


@router.post("", response_model=UserGetSchema, responses={**responses_post_user})
async def create_user(
    response: Response, user: UserCreateSchema, db: AsyncSession = Depends(get_db)
):
    """
    Create user:\n
    user: shame of user to create\n
    db: datebase connection;\n
    """
    new_user = await user_queries.create(db=db, user_schema=user)
    response.status_code = 201
    return UserGetSchema(**new_user.__dict__)


@router.put("", response_model=UserGetSchema, responses={**responses_update_user})
async def update_user(
    user: UserUpdateSchema,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    update user:\n
    user: dataset of UserUpdateSchema\n
    db: datebase connection;\n
    current_user: only for autorized user\n
    """
    old_user = await user_queries.get_by_id(db=db, user_id=current_user.id)

    old_user.name = user.name if user.name is not None else old_user.name
    old_user.email = user.email if user.email is not None else old_user.email
    old_user.is_company = user.is_company if user.is_company is not None else old_user.is_company

    new_user = await user_queries.update(db=db, user=old_user)

    return UserGetSchema(**new_user.__dict__)


@router.delete("", response_model=UserGetSchema, responses={**responses_delete_user})
async def delete_user(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Delete current user:\n
    db: datebase connection;\n
    current_user:current user\n
    """
    removed_user = await user_queries.delete(db=db, delete_user=current_user)
    return UserGetSchema(**removed_user.__dict__)
