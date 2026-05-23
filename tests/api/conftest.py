import pytest
from core.utils.api_client import APIClient
from tests.api.helpers.auth import register_and_login


@pytest.fixture
def api_client():
    """A fresh APIClient with no auth. 
    Use for testing endpoints that don't require login."""
    return APIClient()


@pytest.fixture(scope="session")
def registered_user():
    """Returns (payload, token) for a seeded user. Created once per session."""
    return register_and_login()


@pytest.fixture
def auth_client(registered_user):
    """An APIClient that has completed login with a valid token (no session cookies) 
    - returns the client itself."""
    _, token = registered_user
    return APIClient(token=token)
