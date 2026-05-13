import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app

@pytest.fixture
def anyio_backend():
    return "asyncio"

@pytest.fixture
async def client():
    transport = ASGITransport(app=app)
    
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client


@pytest.fixture(autouse=True)
def clear_db():
    from app.main import fake_db, next_id
    
    fake_db.clear()
    
    next_id = 1
    
    yield  
    
@pytest.fixture
def faker_instance():
    from faker import Faker
    return Faker()