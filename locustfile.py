from locust import  HttpUser, task, between
import os
from dotenv import load_dotenv

load_dotenv()

class SaaSUser(HttpUser):
    wait_time = between(1,3)
    token = None

    def on_start(self):
        "Login once when the user starts."
        response = self.client.post("/auth/login", json={
            "email": os.getenv("LOC_EMAIL"),
            "password": os.getenv("LOC_PASS")
        })
        if response.status_code == 200:
            self.token = response.json()["access_token"]

    def auth_headers(self):
        return {"Authorization": f"Bearer {self.token}"}

    @task(3)
    def get_tasks(self):
        "Most common operation — weighted 3x."
        self.client.get("/organization/1/tasks", headers=self.auth_headers())

    @task(1)
    def create_task(self):
        "Create a task — weighted 1x."
        self.client.post("/organization/1/tasks", json={
            "title": "Load test task",
            "description": "Created by locust",
            "priority": "low",
            "status": "pending",
            "due_date": "2027-01-01T00:00:00Z"
        }, headers=self.auth_headers())

    @task(2)
    def get_org(self):
        "Get org details — weighted 2x."
        self.client.get("/organization/1", headers=self.auth_headers())