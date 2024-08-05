import os

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")
DB_HOST = os.environ.get("DB_HOST")
DB_NAME = os.environ.get("DB_NAME")
DB_PORT = os.environ.get("DB_PORT")

test_mode = False
if os.environ.get("test_mode"):
    test_mode = True

DB_USER_TEST = os.environ.get("DB_USER_TEST")
DB_PASS_TEST = os.environ.get("DB_PASS_TEST")
DB_HOST_TEST = os.environ.get("DB_HOST_TEST")
DB_NAME_TEST = os.environ.get("DB_NAME_TEST")
DB_PORT_TEST = os.environ.get("DB_PORT_TEST")

SQLALCHEMY_DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
SQLALCHEMY_DATABASE_URL_TEST = f"postgresql+asyncpg://{DB_USER_TEST}:{DB_PASS_TEST}@{DB_HOST_TEST}:{DB_PORT_TEST}/{DB_NAME_TEST}"
engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True)

SessionLocal = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)
)

Base = declarative_base()
