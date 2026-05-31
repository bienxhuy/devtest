import pytest
from core.utils.logs import get_logger
from tests.api.helpers.api_endpoints import APIEndpoints
from tests.api.mock_data.users import UserPayloadBuilder


logger = get_logger()


@pytest.fixture
def fresh_user():
    """A unique user registered for one test. Not reused across tests."""
    payload = UserPayloadBuilder().build()
    logger.debug(f"[API_FIXTURES] Built fresh user payload for {payload['email']}")
    return payload


# This fixture doesn't reuse registered users, 
# Because if some tests are executed before the logout tests, 
# they might invalidate the refresh token for the shared user, 
# causing logout tests to fail unexpectedly.
# Scope is function-level by default, so each test doesn't affect others session.
@pytest.fixture
def cookie_jar(fresh_user, api_client):
    """An APIClient that has completed login 
    - session holds refreshToken cookie and access token.
    - Return (client)."""
    logger.info(f"[API_FIXTURES] Registering cookie-jar user {fresh_user['email']}")
    api_client.post(APIEndpoints.register, json=fresh_user)
    res = api_client.post(APIEndpoints.login, json={
        "email": fresh_user["email"],
        "password": fresh_user["password"]
    })
    res.raise_for_status()
    payload = res.json()
    token = payload["data"]["accessToken"]
    api_client.set_token(token)
    logger.info(f"[API_FIXTURES] Cookie-jar user authenticated: {fresh_user['email']}")
    return api_client
