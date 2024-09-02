from dataclasses import asdict

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException, status

from dependencies import get_current_user
from dependencies.containers import RepositoriesContainer
from models import User
from repositeries import UserRepository
from tools.security import hash_password
from web.schemas import UserCreateSchema, UserSchema, UserUpdateSchema

router = APIRouter(prefix="/users", tags=["users"])


@router.get("")
@inject
async def read_users(
    limit: int = 100,
    skip: int = 0,
    user_repository: UserRepository = Depends(Provide[RepositoriesContainer.user_repository]),
) -> list[UserSchema]:
    users_model = await user_repository.retrieve_many(limit, skip)

    users_schema = []
    for model in users_model:
        users_schema.append(
            UserSchema(
                id=model.id,
                name=model.name,
                email=model.email,
                is_company=model.is_company,
            )
        )
    return users_schema


@router.post("")
@inject
async def create_user(
    user_create_dto: UserCreateSchema,
    user_repository: UserRepository = Depends(Provide[RepositoriesContainer.user_repository]),
) -> UserSchema:
    user = await user_repository.create(
        user_create_dto, hashed_password=hash_password(user_create_dto.password)
    )
    return UserSchema(**asdict(user))


@router.put("")
@inject
async def update_user(
    user_update_schema: UserUpdateSchema,
    user_repository: UserRepository = Depends(Provide[RepositoriesContainer.user_repository]),
    current_user: User = Depends(get_current_user),
) -> UserSchema:

    existing_user = await user_repository.retrieve(email=user_update_schema.email)
    if existing_user and existing_user.id != current_user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Недостаточно прав")

    try:
        updated_user = await user_repository.update(current_user.id, user_update_schema)
        return UserSchema(**asdict(updated_user))

    except ValueError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь не найден")
