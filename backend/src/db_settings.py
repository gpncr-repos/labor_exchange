from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_scoped_session
from sqlalchemy.ext.declarative import declarative_base
from asyncio import current_task
import os

from sqlalchemy.orm import sessionmaker

DB_USER = os.environ.get("DB_USER", "admin")
DB_PASS = os.environ.get("DB_PASS", "admin")
DB_HOST = os.environ.get("DB_HOST", "localhost")

if os.environ.get("DB_STAGE") == 'test':
    DB_NAME = os.environ.get("DB_NAME", "labor-exchange-test")
    DB_PORT = '5430'
else:
    DB_NAME = os.environ.get("DB_NAME", "labor-exchange")
    DB_PORT = '5432'


SQLALCHEMY_DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL,
)

SessionLocal = async_scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession), scopefunc=current_task)

Base = declarative_base()
