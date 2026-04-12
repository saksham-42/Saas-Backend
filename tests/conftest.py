import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.core.db import Base, get_database
from app.core.config import settings

engine = create_engine(settings.TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="session", autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def db():
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture(scope="function")
def client(db):
    def override_get_database():
        yield db
    app.dependency_overrides[get_database] = override_get_database
    yield TestClient(app)
    app.dependency_overrides.clear()

def create_user_and_token(client, email, name="Test User", age=25, password="secret123"):
    client.post("/auth/register", json={
        "name": name, "age": age, "email": email, "password": password
    })
    login = client.post("/auth/login", json={"email": email, "password": password})
    token = login.json()["access_token"]
    return token

def auth_headers(token):
    return {"Authorization": f"Bearer {token}"}

@pytest.fixture
def admin_token(client, db):
    from app.crud.users import get_user_by_email
    create_user_and_token(client, "admin@example.com")
    user = get_user_by_email(db, "admin@example.com")
    user.role = "admin"
    db.commit()
    login = client.post("/auth/login", json={"email": "admin@example.com", "password": "secret123"})
    return login.json()["access_token"]

@pytest.fixture
def member_token(client):
    return create_user_and_token(client, "member@example.com")

@pytest.fixture
def other_user_token(client):
    return create_user_and_token(client, "other@example.com")

@pytest.fixture
def org(client, admin_token):
    response = client.post("/organization/", json={
        "name": "Test Org", "slug": "test-org"
    }, headers=auth_headers(admin_token))
    return response.json()

@pytest.fixture
def other_org(client, other_user_token):
    response = client.post("/organization/", json={
        "name": "Other Org", "slug": "other-org"
    }, headers=auth_headers(other_user_token))
    return response.json()

@pytest.fixture
def task(client, admin_token, org):
    response = client.post(f"/organization/{org['id']}/tasks", json={
        "title": "Test Task",
        "description": "A task",
        "status": "pending",
        "priority": "medium",
        "assigned_to": None,
        "due_date": None
    }, headers=auth_headers(admin_token))
    return response.json()