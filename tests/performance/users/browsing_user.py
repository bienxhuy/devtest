from locust import task, between

from .base_user import BasePerfUser


class BrowsingUser(BasePerfUser):
    """Unauthenticated users reading public quotes."""

    weight = 5
    wait_time = between(2, 5)

    @task
    def get_quotes_default(self):
        self.client.get("/api/quotes", name="/api/quotes")

    @task
    def get_quotes_page_2(self):
        self.client.get(
            "/api/quotes?page=2&limit=10",
            name="/api/quotes [paginated]",
        )
