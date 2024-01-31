from fastapi import APIRouter, HTTPException, status, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession
from applications.queries import user as user_queries

from presentations.schemas.auth import TokenSchema, LoginSchema
from core.security import verify_password, create_access_token
from applications.dependencies import get_db


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("")#, response_model=TokenSchema)
async def login(response: Response, login: LoginSchema, db: AsyncSession = Depends(get_db)):
    user = await user_queries.get_by_email(db=db, email=login.email)

    if user is None or not verify_password(login.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Некорректное имя пользователя или пароль")

    access_token = create_access_token({"sub":user.email})
    response.set_cookie("access_token", access_token, httponly=True)
    return TokenSchema(
        access_token=access_token, #create_access_token({"sub": user.email}),
        token_type="Bearer"
    )
