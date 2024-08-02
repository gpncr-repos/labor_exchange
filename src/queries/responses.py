from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import Response
from schemas import ResponsesSchema, ResponsestoSchema


async def get_response_by_job_id(
    db: AsyncSession, job_id: int
) -> list[ResponsesSchema]:
    query = select(Response).where(Response.job_id == job_id)
    res = await db.execute(query)
    return res.scalars().all()


async def get_response_by_user_id(
    db: AsyncSession, user_id: int
) -> list[ResponsesSchema]:
    query = select(Response).where(Response.user_id == user_id)
    res = await db.execute(query)
    return res.scalars().all()


async def get_response_by_job_id_and_user_id(
    db: AsyncSession, job_id: int, user_id: int
) -> ResponsesSchema:
    query = select(Response).where(
        Response.job_id == job_id and Response.user_id == user_id
    )
    res = await db.execute(query)
    return res.scalars().first()


async def response_create(
    db: AsyncSession, response_schema: ResponsestoSchema, user_id: int
) -> Response:
    response_el = Response(
        user_id=user_id,
        job_id=response_schema.job_id,
        massage=response_schema.massage,
    )
    db.add(response_el)
    await db.commit()
    await db.refresh(response_el)
    return response_el


async def update(db: AsyncSession, response: ResponsesSchema) -> ResponsesSchema:
    db.add(response)
    await db.commit()
    await db.refresh(response)
    return response


async def delete(db: AsyncSession, response: ResponsesSchema) -> ResponsesSchema:
    id = response.id
    await db.delete(response)
    await db.commit()
    res = await get_response_by_id(db=db, response_id=id)
    return res


async def get_response_by_id(db: AsyncSession, response_id: int) -> ResponsesSchema:
    query = select(Response).where(Response.id == response_id)
    res = await db.execute(query)
    return res.scalars().first()
