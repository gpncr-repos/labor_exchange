from fastapi import APIRouter, HTTPException, status, Depends, Response, Request
from fastapi.responses import JSONResponse
from fastapi_jwt_auth.exceptions import AuthJWTException
from sqlalchemy.ext.asyncio import AsyncSession
from applications.queries import user_queries as user_queries

from api.schemas.auth import TokenSchema, LoginSchema, TokenSchemaPair
from core.security import verify_password, create_access_token
from applications.dependencies import get_db


router = APIRouter(prefix="/auth", tags=["auth"])


# @router.post("")#, response_model=TokenSchema)
# async def login(response: Response, login: LoginSchema, db: AsyncSession = Depends(get_db)):
#     user = await user_queries.get_by_email(db=db, email=login.email)
#
#     if user is None or not verify_password(login.password, user.hashed_password):
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Некорректное имя пользователя или пароль")
#
#     access_token = create_access_token({"sub":user.email})
#     response.set_cookie("access_token", access_token, httponly=True)
#     return TokenSchema(
#         access_token=access_token, #create_access_token({"sub": user.email}),
#         token_type="Bearer"
#     )

# @router.post("")#, response_model=TokenSchema)
# async def login(response: Response, login: LoginSchema, db: AsyncSession = Depends(get_db)):
#     user = await user_queries.get_by_email(db=db, email=login.email)
#
#     if user is None or not verify_password(login.password, user.hashed_password):
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Некорректное имя пользователя или пароль")
#
#     access_token = create_access_token({"sub":user.email})
#     refresh_token = create_access_token({"sub":user.email})
#     response.set_cookie("access_token", access_token, httponly=True)
#     return TokenSchemaPair(
#         access_token=TokenSchema(token=access_token,
#                     token_type="Bearer"),
#         refresh_token=TokenSchema(token=refresh_token,
#                     token_type="Bearer")
#     )

from fastapi_jwt_auth import AuthJWT
from core.security import SECRET_KEY
from pydantic import BaseModel

class Settings(BaseModel):
    authjwt_secret_key: str = SECRET_KEY

@AuthJWT.load_config
def get_secret_key():
    return Settings()

@router.post("/login", response_model=TokenSchemaPair)
async def login(
        login: LoginSchema,
        db: AsyncSession = Depends(get_db),
        Authorize: AuthJWT = Depends()
    ):
    user = await user_queries.get_by_email(db, login.email)

    if user is None or not verify_password(login.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Некорректное имя пользователя или пароль")

    access_token = Authorize.create_access_token(subject=login.email)
    refresh_token = Authorize.create_refresh_token(subject=login.email)
    return TokenSchemaPair(
        access_token=TokenSchema(token=access_token, token_type="Bearer"),
        refresh_token=TokenSchema(token=refresh_token, token_type="Bearer")
    )

# @router.exception_handler(AuthJWTException)
# def authjwt_exception_handler(request: Request, exc: AuthJWTException):
#     return JSONResponse(
#         status_code=exc.status_code,
#         content={"detail": exc.message}
#     )


@router.post("/refresh", summary="Получение нового access_token'а")
def refresh(Authorize: AuthJWT = Depends()):
    Authorize.jwt_refresh_token_required()
    current_user = Authorize.get_jwt_subject()
    new_access_token = Authorize.create_access_token()
    return TokenSchema(
        token=new_access_token, token_type="Bearer"
    )

@router.get('/user111')
def user(Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()

    current_user = Authorize.get_jwt_subject()
    return {"user": current_user}
