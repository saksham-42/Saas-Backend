from tests.conftest import auth_headers, create_user_and_token


def test_get_all_users(client, admin_token):
    response = client.get("/api/v1/users/", headers=auth_headers(admin_token))
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_user_by_id(client, admin_token):
    reg = client.post("/api/v1/auth/register", json={
        "name": "Find Me", "age": 25,
        "email": "findme@example.com", "password": "secret123"
    })
    users = client.get("/api/v1/users/", headers=auth_headers(admin_token)).json()
    user_id = next(u["id"] for u in users if u["email"] == "findme@example.com")
    response = client.get(f"/api/v1/users/{user_id}", headers=auth_headers(admin_token))
    assert response.status_code == 200
    assert response.json()["email"] == "findme@example.com"


def test_get_user_not_found(client, admin_token):
    response = client.get("/api/v1/users/99999", headers=auth_headers(admin_token))
    assert response.status_code == 404


def test_update_user(client, admin_token):
    client.post("/api/v1/auth/register", json={
        "name": "Old Name", "age": 25,
        "email": "update@example.com", "password": "secret123"
    })
    users = client.get("/api/v1/users/", headers=auth_headers(admin_token)).json()
    user_id = next(u["id"] for u in users if u["email"] == "update@example.com")
    response = client.put(f"/api/v1/users/{user_id}", json={
        "name": "New Name", "age": 30
    }, headers=auth_headers(admin_token))
    assert response.status_code == 200
    assert response.json()["name"] == "New Name"


def test_get_my_tasks(client, admin_token, org):
    response = client.get("/api/v1/users/me/tasks", headers=auth_headers(admin_token))
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_me(client, admin_token):
    response = client.get("/api/v1/users/me", headers=auth_headers(admin_token))
    assert response.status_code == 200
    assert response.json()["email"] == "admin@example.com"


def test_update_user_not_found(client, admin_token):
    response = client.put("/api/v1/users/99999", json={
        "name": "Ghost", "age": 25
    }, headers=auth_headers(admin_token))
    assert response.status_code == 404