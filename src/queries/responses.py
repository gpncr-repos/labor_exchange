from typing import List

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from models import Response
from schemas import ResponseInSchema


async def response_job(db: AsyncSession, response_schema: ResponseInSchema) -> Response:
    try:
        response = Response(
            user_id=response_schema.user_id,
            job_id=response_schema.job_id,
            message=response_schema.message,
        )
        db.add(response)
        await db.commit()
        await db.refresh(response)
        return response
    except SQLAlchemyError as e:
        await db.rollback()
        raise ValueError("При создании отклика произошла ошибка.") from e


async def get_response_by_user_id(db: AsyncSession, job_id: int) -> List[Response]:
    query = select(Response).where(Response.job_id == job_id)
    res = await db.execute(query)
    return res.scalars().all()
