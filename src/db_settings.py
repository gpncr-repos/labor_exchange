from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
import os

DB_USER = os.environ.get("DB_USER", "admin")
DB_PASS = os.environ.get("DB_PASS", "admin")
DB_HOST = os.environ.get("DB_HOST", "localhost")
DB_PORT = os.environ.get("DB_PORT", "5433")
DB_NAME = os.environ.get("DB_NAME", "labor-exchange")

SQLALCHEMY_DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL
)

SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession))

Base = declarative_base()
