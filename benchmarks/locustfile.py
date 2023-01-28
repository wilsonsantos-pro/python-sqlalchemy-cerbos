from uuid import uuid4

from locust import HttpUser, task


class CerbosUser(HttpUser):
    host = "http://john@localhost:3592"

    @task
    def api_check(self):
        data = {
            "requestId": str(uuid4()),
            "actions": ["read"],
            "resource": {
                "kind": "contact",
                "instances": {"1": {"attr": {"id": "1", "is_active": True}}},
            },
            "principal": {
                "id": "john",
                "roles": ["user"],
                "attr": {"department": "Sales"},
            },
        }
        self.client.post("/api/check", json=data)
