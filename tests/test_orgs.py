from tests.conftest import auth_headers


def test_create_org_duplicate_slug(client, admin_token, org):
    response = client.post("/organization/", json={
        "name": "Another Org", "slug": "test-org"
    }, headers=auth_headers(admin_token))
    assert response.status_code == 400


def test_get_org_success(client, admin_token, org):
    response = client.get(f"/organization/{org['id']}", headers=auth_headers(admin_token))
    assert response.status_code == 200
    assert response.json()["id"] == org["id"]


def test_get_org_not_found(client, admin_token):
    response = client.get("/organization/99999", headers=auth_headers(admin_token))
    assert response.status_code == 403


def test_remove_org_owner_fails(client, admin_token, org):
    users = client.get("/users/", headers=auth_headers(admin_token)).json()
    owner_id = next(u["id"] for u in users if u["email"] == "admin@example.com")
    response = client.delete(f"/organization/{org['id']}/members/{owner_id}", headers=auth_headers(admin_token))
    assert response.status_code == 400


def test_update_member_role(client, admin_token, member_token, org):
    users = client.get("/users/", headers=auth_headers(admin_token)).json()
    member_id = next(u["id"] for u in users if u["email"] == "member@example.com")
    client.post(f"/organization/{org['id']}/members?user_id={member_id}", headers=auth_headers(admin_token))
    response = client.patch(f"/organization/{org['id']}/members/{member_id}/role", json={
        "role": "admin"
    }, headers=auth_headers(admin_token))
    assert response.status_code == 200
    assert response.json()["role"] == "admin"


def test_update_owner_role_fails(client, admin_token, org):
    users = client.get("/users/", headers=auth_headers(admin_token)).json()
    owner_id = next(u["id"] for u in users if u["email"] == "admin@example.com")
    response = client.patch(f"/organization/{org['id']}/members/{owner_id}/role", json={
        "role": "member"
    }, headers=auth_headers(admin_token))
    assert response.status_code == 400


def test_get_org_members(client, admin_token, org):
    response = client.get(f"/organization/{org['id']}/members", headers=auth_headers(admin_token))
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) >= 1