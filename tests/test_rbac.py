from tests.conftest import auth_headers, create_user_and_token


def test_admin_can_delete_user(client, admin_token):
    client.post("/auth/register", json={
        "name": "To Delete", "age": 25,
        "email": "todelete@example.com", "password": "secret123"
    })
    users = client.get("/users/", headers=auth_headers(admin_token))
    user_id = next(u["id"] for u in users.json() if u["email"] == "todelete@example.com")
    response = client.delete(f"/users/{user_id}", headers=auth_headers(admin_token))
    assert response.status_code == 200


def test_non_admin_cannot_delete_user(client, member_token):
    response = client.delete("/users/1", headers=auth_headers(member_token))
    assert response.status_code == 403


def test_non_member_cannot_access_org(client, other_user_token, org):
    response = client.get(f"/organization/{org['id']}", headers=auth_headers(other_user_token))
    assert response.status_code == 403


def test_non_member_cannot_access_org_tasks(client, other_user_token, org):
    response = client.get(f"/organization/{org['id']}/tasks", headers=auth_headers(other_user_token))
    assert response.status_code == 403


def test_data_isolation_org_a_cannot_access_org_b_tasks(client, admin_token, other_user_token, org, other_org):
    client.post(f"/organization/{org['id']}/tasks", json={
        "title": "Org A Task", "description": "secret",
        "status": "pending", "priority": "medium",
        "assigned_to": None, "due_date": None
    }, headers=auth_headers(admin_token))
    response = client.get(f"/organization/{org['id']}/tasks", headers=auth_headers(other_user_token))
    assert response.status_code == 403


def test_only_admin_can_add_members(client, admin_token, member_token, org):
    users = client.get("/users/", headers=auth_headers(admin_token))
    member_id = next(u["id"] for u in users.json() if u["email"] == "member@example.com")
    client.post(f"/organization/{org['id']}/members?user_id={member_id}", headers=auth_headers(admin_token))

    # register a new user explicitly
    client.post("/auth/register", json={
        "name": "New Guy", "age": 25,
        "email": "newguy@example.com", "password": "secret123"
    })
    users = client.get("/users/", headers=auth_headers(admin_token)).json()
    new_user_id = next(u["id"] for u in users if u["email"] == "newguy@example.com")

    # member tries to add — should fail
    response = client.post(f"/organization/{org['id']}/members?user_id={new_user_id}", headers=auth_headers(member_token))
    assert response.status_code == 403

def test_only_admin_can_remove_members(client, admin_token, member_token, org):
    users = client.get("/users/", headers=auth_headers(admin_token))
    member_id = next(u["id"] for u in users.json() if u["email"] == "member@example.com")
    client.post(f"/organization/{org['id']}/members?user_id={member_id}", headers=auth_headers(admin_token))
    response = client.delete(f"/organization/{org['id']}/members/{member_id}", headers=auth_headers(member_token))
    assert response.status_code == 403