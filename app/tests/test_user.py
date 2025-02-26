import random

from fastapi.testclient import TestClient
from app.main import app
from app.config.database import Session
from app.models.user import User
from sqlalchemy.orm import sessionmaker

# Create a test client
client = TestClient(app)


# Dependency override to use test database
def override_get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[Session] = override_get_db


# Test user creation
def test_create_user():
    email: str = f"test{random.randint(5,500)}@example.com"
    response = client.post(
        "/users/",
        json={
            "email": email,
            "password": "12345",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == email


# Test getting all users
def test_get_users():
    response = client.get("/users/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


# Test fetching a specific user
def test_get_user_by_id():
    response = client.get("/users/1")
    assert response.status_code in [200, 404]
