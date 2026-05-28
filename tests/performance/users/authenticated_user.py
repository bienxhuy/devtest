import uuid

from locust import task, between

from helpers.auth_utils import do_login
from .base_user import BasePerfUser


class AuthenticatedUser(BasePerfUser):
    """Logged-in users creating and deleting quotes in a single flow."""

    weight = 3
    wait_time = between(3, 6)

    def on_start(self):
        self.token = do_login(self.client)
        self.headers = {"Authorization": f"Bearer {self.token}"}

    @task
    def create_and_delete(self):
        text = f"lifecycle-{uuid.uuid4().hex[:8]}"
        with self.client.post(
            "/api/quotes",
            json={"text": text},
            headers=self.headers,
            catch_response=True,
            name="/api/quotes [POST]",
        ) as resp:
            if resp.status_code != 201:
                resp.failure(f"Create failed: {resp.status_code}")
                return
            try:
                quote_id = resp.json()["data"]["id"]
            except (KeyError, ValueError):
                resp.failure("Missing id in create response")
                return

        with self.client.delete(
            "/api/quotes",
            json={"id": quote_id},
            headers=self.headers,
            catch_response=True,
            name="/api/quotes [DELETE]",
        ) as resp:
            if resp.status_code != 204:
                resp.failure(f"Delete failed: {resp.status_code}")
