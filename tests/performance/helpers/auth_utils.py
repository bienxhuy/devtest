from locust.exception import RescheduleTask

from .perf_config import PERF_USER_EMAIL, PERF_USER_PASSWORD


def do_login(client):
    """Authenticate and return an access token; reschedule the user on failure."""
    with client.post(
        "/api/auth/login",
        json={"email": PERF_USER_EMAIL, "password": PERF_USER_PASSWORD},
        catch_response=True,
        name="/api/auth/login [setup]",
    ) as resp:
        if resp.status_code == 200:
            try:
                return resp.json()["data"]["accessToken"]
            except (KeyError, ValueError):
                resp.failure("Login response missing accessToken")
                raise RescheduleTask()
        resp.failure(f"Login failed: {resp.status_code}")
        raise RescheduleTask()
