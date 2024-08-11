"""" Model Users API  """

from typing import List

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import get_current_user, get_db
from models import User
from queries import user as user_queries
from schemas import UserCreateSchema, UserGetSchema, UserSchema, UserUpdateSchema

from .validation import Real_Validation

router = APIRouter(prefix="/users", tags=["users"])

responses = {
    204: {"description": "Zero rezult"},
    403: {"description": "You have not power here"},
    422: {"description": "Some proplem with validation"},
}
responses_get = {
    **responses,
    200: {
        "description": "Get user",
        "content": {
            "application/json": {
                "example": {
                    "id": 1,
                    "name": "Vasilii",
                    "email": "Alibabaevich@bandit.cement",
                    "is_company": True,
                    "created_at": "2024-08-06T20:41:48.521Z",
                }
            }
        },
    },
}

responses_post = {
    **responses,
    200: {
        "description": "User create",
        "content": {
            "application/json": {
                "example": {
                    "message": "User created",
                    "user name": "Vasilii",
                    "user email": "Alibabaevich@bandit.cement",
                    "created_at": "2024-08-06T20:41:48.521Z",
                }
            }
        },
    },
}

responses_update = {
    **responses,
    200: {
        "description": "User updated",
        "content": {
            "application/json": {
                "example": {
                    "message": "User updated",
                    "user name": "Alex",
                    "user email": "Belii@bandit.docent",
                    "user is_company": True,
                }
            }
        },
    },
}

responses_delete = {
    **responses,
    200: {
        "description": "User delete",
        "content": {
            "application/json": {
                "example": {
                    "message": "User delete",
                    "user name": "Djady",
                    "user email": "Obi@van.cenoby",
                }
            }
        },
    },
}


@router.get("", response_model=List[UserGetSchema], responses={**responses_get})
async def read_all_users(db: AsyncSession = Depends(get_db), limit: int = 100, skip: int = 0):
    """
    Get limit users skip some:\n
    db: datebase connection;\n
    limit: count of get users,\n
    skip: skip from:\n
    """
    all_users = await user_queries.get_all(db=db, limit=limit, skip=skip)
    Real_Validation.element_not_found(all_users)
    return all_users


@router.get("/{user_id}", response_model=UserSchema, responses={**responses_get})
async def read_users(user_id: int, db: AsyncSession = Depends(get_db)):
    """
    Get user by id:\n
    user_id: user id\n
    db: datebase connection;\n
    """
    user_by_id = await user_queries.get_by_id(db=db, user_id=user_id)
    Real_Validation.element_not_found(user_by_id)
    return user_by_id


@router.post("", response_model=UserCreateSchema, responses={**responses_post})
async def create_user(user: UserCreateSchema, db: AsyncSession = Depends(get_db)):
    """
    Create user:\n
    user: shame of user to create\n
    db: datebase connection;\n
    """
    new_user = await user_queries.create(db=db, user_schema=user)
    return JSONResponse(
        status_code=201,
        content={
            "message": "User created",
            "user name": new_user.name,
            "user email": new_user.email,
            "created at": str(new_user.created_at),
        },
    )


@router.put("", response_model=UserUpdateSchema, responses={**responses_update})
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

    return JSONResponse(
        status_code=200,
        content={
            "message": "User updated",
            "user name": new_user.name,
            "user email": new_user.email,
            "user is_company": new_user.is_company,
        },
    )


@router.delete("", responses={**responses_delete})
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
    return JSONResponse(
        status_code=200,
        content={
            "message": "User delete",
            "user name": removed_user.name,
            "user email": removed_user.email,
        },
    )
