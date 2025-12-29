import os
import sys
from dotenv import load_dotenv
import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy import text
from sqlalchemy.pool import StaticPool
from httpx import AsyncClient, ASGITransport

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Устанавливаем переменные окружения для тестов перед импортом настроек приложения
os.environ["SECRET_KEY"] = "test_secret_key_12345"
os.environ["ALGORITHM"] = "HS256"
os.environ["ACCESS_TOKEN_EXPIRE_MINUTES"] = "30"
os.environ["DB_USER"] = "testuser"
os.environ["DB_PASSWORD"] = "testpass"
os.environ["DB_HOST"] = "localhost"
os.environ["DB_PORT"] = "5432"
os.environ["DB_NAME"] = "testdb"

from app.database import Base, get_db
from main import app
from app.models import Todos, Users
from app.config import Settings
from app import config
from app.routers.auth import bcrypt_context

# Обновляем настройки приложения для тестов
test_settings = Settings()
config.settings = test_settings

# Используем SQLite для тестов, чтобы избежать проблем с подключением к Postgres
# и обеспечить изоляцию тестов.
SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///./testdb.db"

engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = async_sessionmaker(autocommit=False, autoflush=False, expire_on_commit=False, bind=engine)

@pytest_asyncio.fixture(scope="function")
async def async_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    async with TestingSessionLocal() as session:
        yield session
        
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest_asyncio.fixture(scope="function")
async def client(async_db):
    def override_get_db():
        yield async_db

    app.dependency_overrides[get_db] = override_get_db
    
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac
    
    app.dependency_overrides.clear()

@pytest_asyncio.fixture
async def test_user(async_db):
    user = Users(
        username="codingwithrobytest",
        email="codingwithrobytest@email.com",
        first_name="Eric",
        last_name="Roby",
        hashed_password=bcrypt_context.hash("testpassword"),
        role="admin",
        phone_number="(111)-111-1111"
    )
    async_db.add(user)
    await async_db.commit()
    await async_db.refresh(user)
    return user

@pytest_asyncio.fixture
async def test_todo(async_db, test_user):
    todo = Todos(
        title="Learn to code!",
        description="Need to learn everyday!",
        priority=5,
        complete=False,
        owner_id=test_user.id,
    )
    async_db.add(todo)
    await async_db.commit()
    await async_db.refresh(todo)
    return todo

@pytest.fixture
def authenticated_client(client):
    from app.routers.auth import get_current_user
    def override_get_current_user():
        return {'username': 'codingwithrobytest', 'id': 1, 'user_role': 'admin'}
    
    app.dependency_overrides[get_current_user] = override_get_current_user
    yield client
    app.dependency_overrides.pop(get_current_user, None)

@pytest.fixture
def admin_client(client):
    from app.routers.auth import get_current_admin_user
    def override_get_current_admin_user():
        return {'username': 'codingwithrobytest', 'id': 1, 'user_role': 'admin'}
    
    app.dependency_overrides[get_current_admin_user] = override_get_current_admin_user
    yield client
    app.dependency_overrides.pop(get_current_admin_user, None)

@pytest.fixture
def user_client(client):
    from app.routers.auth import get_current_user
    def override_get_current_user():
        return {'username': 'codingwithrobytest', 'id': 1, 'user_role': 'admin'}
    
    app.dependency_overrides[get_current_user] = override_get_current_user
    yield client
    app.dependency_overrides.pop(get_current_user, None)