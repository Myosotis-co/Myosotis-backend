import os
import pytest, asyncio
from fastapi import FastAPI
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from httpx import AsyncClient

from app.main import app
from app.database import Base, SQLALCHEMY_DATABASE_URL
from app.db_manager.seeder import database_seeding
from app.db_manager.db_manage import database_emptying

load_dotenv()
TEST_SQLALCHEMY_DATABASE_URL = f"postgresql+asyncpg://{os.environ.get('POSTGRES_TEST_USER')}:{os.environ.get('POSTGRES_TEST_PASSWORD')}@{os.environ.get('POSTGRES_TEST_HOST')}:{os.environ.get('DATABASE_PORT')}/{os.environ.get('POSTGRES_TEST_DB')}"
TEST_SQLALCHEMY_DATABASE_URL = SQLALCHEMY_DATABASE_URL
async_engine = create_async_engine(TEST_SQLALCHEMY_DATABASE_URL, echo=True)


@pytest.fixture(scope="session")
async def async_db_engine():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield async_engine

    # No dropping for now
    # async with async_engine.begin() as conn:
    #     await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope="function")
async def async_db(async_db_engine):
    async_session = sessionmaker(
        expire_on_commit=False,
        autocommit=False,
        autoflush=False,
        bind=async_db_engine,
        class_=AsyncSession,
    )
    async with async_session() as session:
        await session.begin()
        try:
            yield session
        finally:
            await session.close()


@pytest.fixture(scope="session")
async def async_client() -> AsyncClient:
    return AsyncClient(app=app, base_url="http://localhost:8000")


# Let test session to know it is running inside event loop
@pytest.fixture(scope="session")
def event_loop():
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()
