from tests.conftest import auth_headers


def test_soft_delete_task_not_in_list(client, admin_token, org, task):
    client.delete(f"/organization/{org['id']}/tasks/{task['id']}", headers=auth_headers(admin_token))
    response = client.get(f"/organization/{org['id']}/tasks", headers=auth_headers(admin_token))
    assert response.status_code == 200
    task_ids = [t["id"] for t in response.json()]
    assert task["id"] not in task_ids


def test_pagination_skip(client, admin_token, org):
    for i in range(3):
        client.post(f"/organization/{org['id']}/tasks", json={
            "title": f"Task {i}", "description": None,
            "status": "pending", "priority": "medium",
            "assigned_to": None, "due_date": None
        }, headers=auth_headers(admin_token))
    response = client.get(f"/organization/{org['id']}/tasks?skip=2&limit=10", headers=auth_headers(admin_token))
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_pagination_limit(client, admin_token, org):
    for i in range(5):
        client.post(f"/organization/{org['id']}/tasks", json={
            "title": f"Task {i}", "description": None,
            "status": "pending", "priority": "medium",
            "assigned_to": None, "due_date": None
        }, headers=auth_headers(admin_token))
    response = client.get(f"/organization/{org['id']}/tasks?skip=0&limit=3", headers=auth_headers(admin_token))
    assert response.status_code == 200
    assert len(response.json()) == 3


def test_create_task_with_invalid_assignee(client, admin_token, org):
    response = client.post(f"/organization/{org['id']}/tasks", json={
        "title": "Bad Task", "description": None,
        "status": "pending", "priority": "medium",
        "assigned_to": 99999, "due_date": None
    }, headers=auth_headers(admin_token))
    assert response.status_code == 400


def test_update_task_status(client, admin_token, org, task):
    response = client.put(f"/organization/{org['id']}/tasks/{task['id']}", json={
        "status": "completed"
    }, headers=auth_headers(admin_token))
    assert response.status_code == 200
    assert response.json()["status"] == "completed"


def test_get_tasks_filter_by_status(client, admin_token, org):
    client.post(f"/organization/{org['id']}/tasks", json={
        "title": "Pending Task", "description": None,
        "status": "pending", "priority": "medium",
        "assigned_to": None, "due_date": None
    }, headers=auth_headers(admin_token))
    response = client.get(f"/organization/{org['id']}/tasks?status=pending", headers=auth_headers(admin_token))
    assert response.status_code == 200
    assert all(t["status"] == "pending" for t in response.json())

def test_assign_task(client, admin_token, member_token, org, task):
    users = client.get("/users/", headers=auth_headers(admin_token)).json()
    member_id = next(u["id"] for u in users if u["email"] == "member@example.com")
    client.post(f"/organization/{org['id']}/members?user_id={member_id}", headers=auth_headers(admin_token))
    response = client.patch(f"/organization/{org['id']}/tasks/{task['id']}/assign", json={
        "assigned_to": member_id
    }, headers=auth_headers(admin_token))
    assert response.status_code == 200
    assert response.json()["assigned_to"] == member_id


def test_assign_task_invalid_user(client, admin_token, org, task):
    response = client.patch(f"/organization/{org['id']}/tasks/{task['id']}/assign", json={
        "assigned_to": 99999
    }, headers=auth_headers(admin_token))
    assert response.status_code == 404


def test_get_tasks_empty(client, admin_token, org):
    response = client.get(f"/organization/{org['id']}/tasks", headers=auth_headers(admin_token))
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_delete_already_deleted_task(client, admin_token, org, task):
    client.delete(f"/organization/{org['id']}/tasks/{task['id']}", headers=auth_headers(admin_token))
    response = client.delete(f"/organization/{org['id']}/tasks/{task['id']}", headers=auth_headers(admin_token))
    assert response.status_code == 404


def test_create_task_past_due_date(client, admin_token, org):
    response = client.post(f"/organization/{org['id']}/tasks", json={
        "title": "Past Task", "description": None,
        "status": "pending", "priority": "medium",
        "assigned_to": None,
        "due_date": "2020-01-01T00:00:00Z"
    }, headers=auth_headers(admin_token))
    assert response.status_code == 422


def test_get_tasks_filter_in_progress(client, admin_token, org):
    client.post(f"/organization/{org['id']}/tasks", json={
        "title": "In Progress Task", "description": None,
        "status": "in_progress", "priority": "medium",
        "assigned_to": None, "due_date": None
    }, headers=auth_headers(admin_token))
    response = client.get(f"/organization/{org['id']}/tasks?status=in_progress", headers=auth_headers(admin_token))
    assert response.status_code == 200
    assert all(t["status"] == "in_progress" for t in response.json())