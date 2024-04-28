import pytest
from databases import Database
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from models.good import *
from config import settings

# Создание асинхронного движка для тестовой базы данных
test_engine_url = settings.POSTGRES_TEST_DATABASE_URL
test_engine = create_async_engine(test_engine_url)

# Создание асинхронной сессии для тестов
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine, class_=AsyncSession)

@pytest.fixture(scope="session", autouse=True)
async def create_test_database():
    # Создание тестовой базы данных
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

@pytest.fixture
async def db():
    async with Database(test_engine_url) as database:
        yield database