from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import Response
from schemas import ResponsesCreateSchema, ResponsesSchema


async def get_response_by_job_id(db: AsyncSession, job_id: int) -> List[Response]:
    query = select(Response).where(Response.job_id == job_id)
    res = await db.execute(query)
    return res.scalars().all()


async def get_response_by_user_id(db: AsyncSession, user_id: int) -> List[Response]:
    query = select(Response).where(Response.user_id == user_id)
    res = await db.execute(query)
    return res.scalars().all()


async def get_response_by_id(db: AsyncSession, response_id: int) -> Optional[Response]:
    query = select(Response).where(Response.id == response_id)
    res = await db.execute(query)
    return res.scalars().first()


async def get_response_by_job_id_and_user_id(
    db: AsyncSession, job_id: int, user_id: int
) -> Optional[Response]:
    query = select(Response).where(Response.job_id == job_id and Response.user_id == user_id)
    res = await db.execute(query)
    return res.scalars().first()


async def response_create(
    db: AsyncSession, response_schema: ResponsesCreateSchema, user_id: int
) -> Optional[Response]:
    response_el = Response(
        user_id=user_id,
        job_id=response_schema.job_id,
        message=response_schema.message,
    )
    db.add(response_el)
    await db.commit()
    await db.refresh(response_el)
    return response_el


async def update(db: AsyncSession, response: ResponsesSchema) -> Optional[Response]:
    db.add(response)
    await db.commit()
    await db.refresh(response)
    update_response_id = response.id
    res = await get_response_by_id(db=db, response_id=update_response_id)
    return res


async def delete(db: AsyncSession, response: ResponsesSchema) -> Optional[ResponsesSchema]:
    await db.delete(response)
    await db.commit()
    return response
