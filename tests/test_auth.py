from jose import jwt
from datetime import datetime, timedelta, timezone
from app.core.config import settings


def test_tampered_token(client):
    response = client.get("/users/me", headers={
        "Authorization": "Bearer faketoken.tampered.signature"
    })
    assert response.status_code == 401


def test_expired_token(client):
    expired_token = jwt.encode(
        {"sub": "test@example.com", "exp": datetime.now(timezone.utc) - timedelta(minutes=1)},
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )
    response = client.get("/users/me", headers={
        "Authorization": f"Bearer {expired_token}"
    })
    assert response.status_code == 401

def test_register(client):
    response = client.post("/auth/register", json={
        "name": "Test User",
        "age": 25,
        "email": "test@example.com",
        "password": "secret123"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@example.com"
    assert data["name"] == "Test User"


def test_register_duplicate_email(client):
    payload = {
        "name": "Test User",
        "age": 25,
        "email": "duplicate@example.com",
        "password": "secret123"
    }
    client.post("/auth/register", json=payload)
    response = client.post("/auth/register", json=payload)
    assert response.status_code == 400


def test_login_success(client):
    client.post("/auth/register", json={
        "name": "Test User",
        "age": 25,
        "email": "login@example.com",
        "password": "secret123"
    })
    response = client.post("/auth/login", json={
        "email": "login@example.com",
        "password": "secret123"
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"


def test_login_wrong_password(client):
    client.post("/auth/register", json={
        "name": "Test User",
        "age": 25,
        "email": "wrongpass@example.com",
        "password": "secret123"
    })
    response = client.post("/auth/login", json={
        "email": "wrongpass@example.com",
        "password": "wrongpassword"
    })
    assert response.status_code == 401


def test_login_nonexistent_user(client):
    response = client.post("/auth/login", json={
        "email": "nobody@example.com",
        "password": "secret123"
    })
    assert response.status_code == 401


def test_protected_route_without_token(client):
    response = client.get("/users/me")
    assert response.status_code == 401


def test_protected_route_with_token(client):
    client.post("/auth/register", json={
        "name": "Test User",
        "age": 25,
        "email": "protected@example.com",
        "password": "secret123"
    })
    login = client.post("/auth/login", json={
        "email": "protected@example.com",
        "password": "secret123"
    })
    token = login.json()["access_token"]
    response = client.get("/users/me", headers={
        "Authorization": f"Bearer {token}"
    })
    assert response.status_code == 200