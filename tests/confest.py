# Drops the whole database, not cool

# import pytest
# from httpx import AsyncClient
# from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
# from sqlalchemy.orm import sessionmaker

# from app.config import settings
# from app.database import Base, engine
# from app.email.models import TempEmail
# from app.main import app

# engine = create_async_engine(
#     f"postgresql+asyncpg://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_HOST}:{settings.DATABASE_PORT}/{settings.POSTGRES_DB}",
#     echo=True,
# )


# @pytest.fixture
# async def async_db_engine():
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)

#     yield engine

#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.drop_all)


# @pytest.fixture(scope="function")
# async def async_db(async_db_engine):
#     async_session = sessionmaker(
#         expire_on_commit=False,
#         autocommit=False,
#         autoflush=False,
#         bind=async_db_engine,
#         class_=AsyncSession,
#     )

#     async with async_session() as session:
#         await session.begin()

#         yield session

#         await session.rollback()

#         for table in reversed(Base.metadata.sorted_tables):
#             await session.execute(f"TRUNCATE {table.name} CASCADE;")
#             await session.commit()


# @pytest.fixture
# async def async_client() -> AsyncClient:
#     return AsyncClient(app=app, base_url="http://localhost")


# @pytest.fixture
# async def generate_email(async_db: AsyncSession):
#     email = TempEmail(email="test@gmail.com")
#     async_db.add(email)
#     await async_db.commit()
#     await async_db.refresh(email)
#     return email
