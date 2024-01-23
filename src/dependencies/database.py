from src.database.engine import SessionLocal


async def get_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        await db.close()
