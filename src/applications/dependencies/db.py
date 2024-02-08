from db_settings import SessionLocal


async def get_db():
    """Возвращает объект сессию для связи с базой данных;  впоследствии закрывает сессию"""
    db = SessionLocal()
    try:
        yield db
    finally:
        await db.close()