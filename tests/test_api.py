import pytest
from databases import Database
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from models.good import Base  # Импорт Base из models.good
from config import settings
from httpx import AsyncClient

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


# Фикстура для создания асинхронного клиента для тестов
@pytest.fixture
async def client():
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client

# Тест для проверки создания автора
@pytest.mark.asyncio
async def test_create_author(client: AsyncClient):
    response = await client.post("/api/authors/", json={"name": "Test Author", "birth_year": 1990})
    assert response.status_code == 201  # Проверяем успешный статус код
    data = response.json()
    assert data["name"] == "Test Author"  # Проверяем, что автор был добавлен
    assert "author_id" in data  # Проверяем, что в ответе есть идентификатор автора

# Тест для получения автора по его идентификатору
@pytest.mark.asyncio
async def test_get_author(client: AsyncClient):
    # Создаем тестового автора
    response = await client.post("/api/authors/", json={"name": "Test Author", "birth_year": 1990})
    assert response.status_code == 201
    data = response.json()
    author_id = data["author_id"]

    # Получаем автора по его идентификатору
    response = await client.get(f"/api/authors/{author_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Author"
    assert data["author_id"] == author_id

# Тест для создания книги
@pytest.mark.asyncio
async def test_create_book(client: AsyncClient):
    author_id = 1
    response = await client.post("/api/books/", json={"title": "Test Book", "publication_year": 2022, "author_id": author_id})
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Book"
    assert data["author_id"] == author_id
    assert "book_id" in data

@pytest.mark.asyncio
async def test_get_all_books(client: AsyncClient):
    response = await client.get("/api/books/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

# Тест для удаления книги
@pytest.mark.asyncio
async def test_delete_book(client: AsyncClient):
    book_id = 1
    response = await client.delete(f"/api/books/{book_id}")
    assert response.status_code == 200
