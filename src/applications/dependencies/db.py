from db_settings import SessionLocal
from infrastructure.repos import RepoJob


async def get_db():
    """Возвращает объект сессию для связи с базой данных;  впоследствии закрывает сессию"""
    db = SessionLocal()
    try:
        yield db
    finally:
        await db.close()
async def get_repo_job():
    """Возвращает объект сессию для связи с базой данных;  впоследствии закрывает сессию"""
    db = SessionLocal()
    try:
        yield RepoJob(db)
    finally:
        await db.close()