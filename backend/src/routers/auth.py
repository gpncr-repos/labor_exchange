from fastapi import APIRouter, HTTPException, status, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from queries import user as user_queries

from schemas import TokenSchema, LoginSchema
from core.security import verify_password, create_access_token
from dependencies import get_db

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("", response_model=TokenSchema)
async def login(login: LoginSchema, db: AsyncSession = Depends(get_db)):
    user = await user_queries.get_by_email(db=db, email=login.email)

    if user is None or not verify_password(login.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Некорректное имя пользователя или пароль")

    return TokenSchema(
        id=user.id,
        username=user.name,
        is_company=user.is_company,
        access_token=create_access_token({"sub": user.email}),
    )


# @router.post("/refresh", response_model=TokenSchema)
# async def refresh_token(token: str = Query(..., description="Access token to refresh")):
#     new_token = refresh_access_token(token)
#     return TokenSchema(
#         access_token=new_token,
#         token_type="Bearer"
#     )