import pytest
from core.utils.api_client import APIClient
from core.utils.logs import get_logger
from tests.api.helpers.auth import register_and_login
import os
from dotenv import load_dotenv


logger = get_logger()
load_dotenv()


@pytest.fixture(scope="session")
def base_url():
    return os.getenv("BE_URL")

@pytest.fixture
def api_client(base_url):
    """A fresh APIClient with no auth. 
    Use for testing endpoints that don't require login."""
    logger.info("[API_FIXTURES] Creating unauthenticated API client")
    return APIClient(base_url=base_url)


@pytest.fixture(scope="session")
def registered_user(base_url):
    """Returns (payload, token) for a seeded user. Created once per session."""
    logger.info("[API_FIXTURES] Creating session-scoped registered user")
    return register_and_login(base_url)


@pytest.fixture
def auth_client(registered_user, base_url):
    """An APIClient that has completed login with a valid token (no session cookies) 
    - returns the client itself."""
    _, token = registered_user
    logger.info("[API_FIXTURES] Creating authenticated API client")
    return APIClient(base_url=base_url, token=token)


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
