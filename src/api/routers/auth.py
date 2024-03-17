from fastapi import APIRouter, HTTPException, status, Depends, Response, Request
from sqlalchemy.ext.asyncio import AsyncSession
from applications.queries import user_queries as user_queries

from api.schemas.auth import TokenSchema, LoginSchema, TokenSchemaPair
from core.security import verify_password, create_access_token, decode_token, SIGNATURE_EXPIRED, JWTBearer, \
    create_refresh_token
from applications.dependencies import get_db


router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("", response_model=TokenSchemaPair, summary="Зарегистрироваться и получить пару токенов access, refresh")
async def login(login: LoginSchema, db: AsyncSession = Depends(get_db)):
    """
    Создает и возвращает пару access и refresh токенов для пользователя, на основе его учетных данных (логина и пароля)

    :param login: LoginSchema пара логин-пароль авторизующегося пользователя
    :param db: AsyncSession объект сессия для работы с базой данных
    :raises: HTTPException: пользователь отсутствует в базе
    :returns: объект, содержащий access_token и refresh_token
    :rtype: TokenSchemaPair
    """
    user = await user_queries.get_by_email(db=db, email=login.email)

    if user is None or not verify_password(login.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Некорректное имя пользователя или пароль")

    access_token = create_access_token({"sub":user.email})
    refresh_token = create_refresh_token({"sub":user.email})
    return TokenSchemaPair(
        access_token=TokenSchema(token=access_token,
                    token_type="Bearer"),
        refresh_token=TokenSchema(token=refresh_token,
                    token_type="Bearer")
    )

@router.post("/refresh", response_model=TokenSchema, summary="Получить новый access_token на основе refresh_token")
# async def login(refresh_token: RefreshSchema, db: AsyncSession = Depends(get_db)):
async def refresh(refresh_token: str = Depends(JWTBearer()), db: AsyncSession = Depends(get_db)):
    """
    Проверяет, что срок действия переданного refresh_token еще не истек.

    Генерирует и возвращает access_token на основе пользовательских данных из refresh_token
    :param refresh_token: str токен длительного действия
    :raises: HTTPException: токен на получен или просрочен
    :returns: access_token
    :rtype: TokenSchema
    """
    r_token = decode_token(refresh_token)

    if r_token is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Невалидный refresh токен")
    elif r_token == SIGNATURE_EXPIRED:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Истек срок действия refresh токена; перерегистрируйтесь")
    else:
        user = await user_queries.get_by_email(db=db, email=r_token.get("sub"))
        access_token = create_access_token({"sub":user.email})
        return TokenSchema(token=access_token,
                        token_type="Bearer")
