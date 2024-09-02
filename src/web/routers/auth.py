from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException, status

from dependencies.containers import RepositoriesContainer
from repositories import UserRepository
from tools.security import create_access_token, verify_password
from web.schemas import LoginSchema, TokenSchema

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("", response_model=TokenSchema)
@inject
async def login(
    login_data: LoginSchema,
    users_repository: UserRepository = Depends(Provide[RepositoriesContainer.user_repository]),
):
    user = await users_repository.retrieve(email=login_data.email, include_relations=False)

    if user is None or not verify_password(login_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Некорректное имя пользователя или пароль",
        )

    return TokenSchema(access_token=create_access_token({"sub": user.email}), token_type="Bearer")
