import pytest
from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture(autouse=True)
def clear_db():
    from app.main import fake_db, next_id
    
    fake_db.clear()
    next_id = 1
    
    yield 