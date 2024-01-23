from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

from src.settings.database import DataBaseSettings

settings = DataBaseSettings()


SQLALCHEMY_DATABASE_URL = (
    f"postgresql+asyncpg://{settings.user}:{settings.password}@{settings.host}:{settings.port}/{settings.name}"
)

engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=settings.echo)

SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession))

Base = declarative_base()
