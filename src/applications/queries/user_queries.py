from applications.command import CommandResult
from infrastructure.repos import RepoUser
from models import User
from api.schemas import UserInSchema
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from core.security import hash_password


async def get_all(db: AsyncSession, limit: int = 100, skip: int = 0) -> List[User]:
    query = select(User).limit(limit).offset(skip)
    res = await db.execute(query)
    return res.scalars().all()


async def get_by_id(db: AsyncSession, id: int) -> Optional[User]:
    query = select(User).where(User.id == id).limit(1)
    res = await db.execute(query)
    return res.scalars().first()


async def create(db: AsyncSession, user_schema: UserInSchema) -> CommandResult:
    user = User(
        name=user_schema.name,
        email=user_schema.email,
        hashed_password=hash_password(user_schema.password),
        is_company=user_schema.is_company
    )
    repo_user = RepoUser(db)
    try:
        res = await repo_user.add(user)
        return CommandResult.success(result=res)
    except Exception as e:
        msg = "Ошибка при добавлении объекта user"
        return CommandResult.fail(message=msg, exception=str(e))

    # db.add(user)
    # await db.commit()
    # await db.refresh(user)


async def update(db: AsyncSession, user: User) -> CommandResult:    # User:
    try:
        await db.merge(user)  # add(user) # TODO: check, debug
        await db.commit()
        # await db.flush(user)
        await db.refresh(user)
        return CommandResult.success(result=user)
    except Exception as e:
        msg = "Ошибка в ходе редактирования пользователя %s, %s" % (user.id, user.name)
        return CommandResult.fail(message=msg, exception=str(e))

async def update_current_user(
        id: int,
        user: User,
        db: AsyncSession,
        current_user: User) -> CommandResult:
    old_user = await get_by_id(db=db, id=id)

    if old_user is None or old_user.email != current_user.email:
        msg= "Пользователь не найден"
        return CommandResult.fail(message=msg)

    old_user.name = user.name if user.name is not None else old_user.name
    old_user.email = user.email if user.email is not None else old_user.email
    old_user.is_company = user.is_company if user.is_company is not None else old_user.is_company

    result = await update(db=db, user=old_user)
    return result

async def get_by_email(db: AsyncSession, email: str) -> User:
    query = select(User).where(User.email == email).limit(1)
    res = await db.execute(query)
    user = res.scalars().first()
    return user
