from models import Response
from fastapi import APIRouter, Depends, HTTPException, status
from schemas import ResponsestoSchema,ResponsesSchema
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select


async def get_response_by_job_id(db: AsyncSession, job_id: int) -> ResponsesSchema:
    query = select(Response).where(Response.job_id==job_id)
    res = await db.execute(query)
    return res.scalars().all()

async def response_create(db: AsyncSession, response_schema: ResponsestoSchema) -> Response:
    response_el = Response(
        user_id=response_schema.user_id,
        job_id=response_schema.job_id,
        massage=response_schema.massage,
    )
    db.add(response_el)
    await db.commit()
    await db.refresh(response_el)
    return response_el

