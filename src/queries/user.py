from models import User
from schemas import UserInSchema
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from core.security import hash_password


async def get_all(db: AsyncSession, limit: int = 100, skip: int = 0) -> List[User]:  #todo зачем лимит?
    query = select(User).limit(limit).offset(skip)
    res = await db.execute(query)
    return res.scalars().all()


async def get_by_id(db: AsyncSession, id: int) -> User:
    query = select(User).where(User.id == id)
    res = await db.execute(query)
    return res.scalars().first()


async def create(db: AsyncSession, user_schema: UserInSchema) -> User:
    user = User(
        name=user_schema.name,
        email=user_schema.email,
        hashed_password=hash_password(user_schema.password),
        is_company=user_schema.is_company
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


async def update(db: AsyncSession, user: User) -> User:
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


async def get_by_email(db: AsyncSession, email: str) -> User:
    query = select(User).where(User.email == email)
    res = await db.execute(query)
    user = res.scalars().all()                                            #хммм scalars
    return user
