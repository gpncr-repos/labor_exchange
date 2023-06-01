from sqlalchemy.ext.asyncio import AsyncSession
from models import User


async def create_job(db: AsyncSession, job_schema, current_user: User):
    pass


async def get_all_jobs(db: AsyncSession, limit: int = 100, skip: int = 0):
    pass


async def get_job_by_id(db: AsyncSession, job_id: int):
    pass
