import pytest
import json
from pathlib import Path

from tests_functional.pages.login_page.login_page import LoginPage


def _load_auth_data() -> dict:
    data_path = Path(__file__).resolve().parents[2] / "test_data" / "env_config.json"
    with data_path.open("r", encoding="utf-8") as config_file:
        return json.load(config_file)


# Page object fixtures - return initialized page objects
@pytest.fixture
def login_page(driver):
    """Returns initialized LoginPage. Use when you need a fresh login page."""
    return LoginPage(driver)


@pytest.fixture(scope="session")
def auth_test_data():
    """Provide externalized authentication test data."""
    return _load_auth_data()

# Account fixtures
@pytest.fixture(scope="session")
def regular_user_account(auth_test_data):
    """Provides a valid student account for testing."""
    return auth_test_data["accounts"]["regular_user"]


@pytest.fixture(scope="session")
def invalid_password(auth_test_data):
    """Provides a known invalid password."""
    return auth_test_data["negative_cases"]["invalid_password"]


@pytest.fixture(scope="session")
def sql_injection_payload(auth_test_data):
    """SQL injection payload for security testing."""
    return auth_test_data["security_payloads"]["sql_injection"]


@pytest.fixture(scope="session")
def sql_injection_password(auth_test_data):
    """Password used with SQL injection negative test."""
    return auth_test_data["negative_cases"]["sql_injection_password"]