import logging

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.tables import User
from src.dependencies import get_current_user, get_session
from src.queries import user as user_queries
from src.schemas import UserInSchema, UserSchema, UserUpdateSchema

router = APIRouter(prefix="/users", tags=["users"])


# добавил get_current_user, чтобы запретить получать данные о пользователях незарегистрированным юзерам
@router.get("/get_users", response_model=list[UserSchema])
async def get_users(
    limit: int = 100,
    skip: int = 0,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    logging.info(f"request was received to receive {limit} users, offset {skip}")
    results = await user_queries.get_all_users(session=session, limit=limit, skip=skip)
    logging.info(f"{len(results)} users have been successfully received")
    return results


@router.post("/create_user", response_class=Response)
async def create_user(user: UserInSchema, session: AsyncSession = Depends(get_session)):
    logging.info("request has been received to create a new user")
    await user_queries.create(session=session, user_schema=user)
    logging.info("the user has been successfully created")
    # у фронта уже есть все данные о пользователе (которые приложены в полезную нагрузку)
    # в связи с этим предлагаю не возвращать их, а просто отдавать код ответа, для отрисовки можно использовать данные,
    # ранее вложенные в полезную нагрузку
    return Response(status_code=status.HTTP_201_CREATED)


@router.put("/update_user", response_class=Response)
async def update_user(
    id: int,
    user: UserUpdateSchema,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    logging.info(f"a request was received to update user id {id} data")
    old_user = await user_queries.get_by_id(session=session, id=id, lock=True)

    if old_user is None or old_user.email != current_user.email:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь не найден")
    await user_queries.update(session=session, old_user=old_user, new_user=user)

    logging.info(f"the data of the user id {id} has been updated")

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("/get_user/{id}", response_model=UserSchema)
async def get_user(
    id: int, session: AsyncSession = Depends(get_session), current_user: User = Depends(get_current_user)
):
    logging.info(f"data on the {id} id user has been requested")
    user = await user_queries.get_by_id(session=session, id=id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь не найден")
    logging.info(f"the data on the user {id} id has been received")
    return user
