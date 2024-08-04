"""" Model Users API  """

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import get_current_user, get_db
from models import User
from queries import user as user_queries
from schemas import (UserCreateSchema, UserGetSchema, UserSchema,
                     UserUpdateSchema)

router = APIRouter(prefix="/users", tags=["users"])


@router.get("", response_model=List[UserGetSchema])
async def read_all_users(
    db: AsyncSession = Depends(get_db), limit: int = 100, skip: int = 0
):
    """
    Get limit users skip some:
    db: datebase connection;
    limit: count of get users,
    skip: skip from:
    """
    all_users = await user_queries.get_all(db=db, limit=limit, skip=skip)
    if not all_users:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="There is no user",
        )
    return all_users


@router.get("/{user_id}", response_model=UserSchema)
async def read_users(user_id: int, db: AsyncSession = Depends(get_db)):
    """
    Get user by id:
    user_id: user id
    db: datebase connection;
    """
    user_by_id = await user_queries.get_by_id(db=db, user_id=user_id)
    if not user_by_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not find"
        )
    return user_by_id


@router.post("", response_model=UserGetSchema)
async def create_user(user: UserCreateSchema, db: AsyncSession = Depends(get_db)):
    """
    Create user:
    user: shame of user to create
    db: datebase connection;
    """
    new_user = await user_queries.create(db=db, user_schema=user)
    return UserGetSchema.from_orm(new_user)


@router.put("", response_model=UserUpdateSchema)
async def update_user(
    user: UserUpdateSchema,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    update user:
    user: dataset of UserUpdateSchema
    db: datebase connection;
    current_user: only for autorized user
    """
    old_user = await user_queries.get_by_id(db=db, user_id=current_user.id)

    old_user.name = user.name if user.name is not None else old_user.name
    old_user.email = user.email if user.email is not None else old_user.email
    old_user.is_company = (
        user.is_company if user.is_company is not None else old_user.is_company
    )

    new_user = await user_queries.update(db=db, user=old_user)

    return UserUpdateSchema.from_orm(new_user)


@router.delete("/delete")
async def delete_user(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Delete current user:
    db: datebase connection;
    current_user:current user
    """
    removed_user = await user_queries.delete(db=db, delete_user=current_user)
    return removed_user
