"""" Model Users API  """

from typing import List

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import get_current_user, get_db
from models import User
from queries import user as user_queries
from schemas import (UserCreateSchema, UserGetSchema, UserSchema,
                     UserUpdateSchema)

from .validation import Validation_for_routers

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
        return Validation_for_routers.empty_base(router_name="User")
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
        return Validation_for_routers.element_not_found(f"User id {user_id}")
    return user_by_id


@router.post("/post", response_model=UserGetSchema)
async def create_user(user: UserCreateSchema, db: AsyncSession = Depends(get_db)):
    """
    Create user:
    user: shame of user to create
    db: datebase connection;
    """
    new_user = await user_queries.create(db=db, user_schema=user)
    return JSONResponse(
        status_code=201,
        content={
            "message": "User created",
            "user name": new_user.name,
            "user email": new_user.email,
        },
    )


@router.put("/put", response_model=UserUpdateSchema)
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

    return JSONResponse(
        status_code=200,
        content={
            "message": "User updated",
            "user name": new_user.name,
            "user email": new_user.email,
            "user is_company": new_user.is_company,
        },
    )


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
    return JSONResponse(
        status_code=200,
        content={
            "message": "User delete",
            "user name": removed_user.name,
            "user email": removed_user.email,
        },
    )
