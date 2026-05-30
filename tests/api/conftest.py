import pytest
from core.utils.api_client import APIClient
from core.utils.logs import get_logger
from tests.api.helpers.auth import register_and_login


logger = get_logger()


@pytest.fixture
def api_client():
    """A fresh APIClient with no auth. 
    Use for testing endpoints that don't require login."""
    logger.info("[API_FIXTURES] Creating unauthenticated API client")
    return APIClient()


@pytest.fixture(scope="session")
def registered_user():
    """Returns (payload, token) for a seeded user. Created once per session."""
    logger.info("[API_FIXTURES] Creating session-scoped registered user")
    return register_and_login()


@pytest.fixture
def auth_client(registered_user):
    """An APIClient that has completed login with a valid token (no session cookies) 
    - returns the client itself."""
    _, token = registered_user
    logger.info("[API_FIXTURES] Creating authenticated API client")
    return APIClient(token=token)


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)


@pytest.fixture(autouse=True)
def log_test_boundary(request):
    logger.info(f"[API_TEST] START {request.node.nodeid}")
    yield
    status = "passed"
    if hasattr(request.node, "rep_call"):
        status = request.node.rep_call.outcome
    logger.info(f"[API_TEST] END {request.node.nodeid} -> {status}")
