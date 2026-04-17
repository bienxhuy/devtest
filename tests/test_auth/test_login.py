""" Test login usecase.
"""
import pytest
from logs.logger import get_logger
from POM.login_page.login_page_notifications import LoginPageNotifications as LgNoti


# Get a logger instance for logging within the tests
logger = get_logger()


class TestLogin:
    """Test class for authentication-related tests."""

    # Test auth - test login - 01
    # Test normal login with valid credentials
    def test_regular_login(self, login_page, regular_user_account):
        logger.info("[TEST] test_regular_login starts")
        login_page.login(email=regular_user_account["email"], password=regular_user_account["password"])
        assert login_page.is_logged_in(), "Login verification failed: User not logged in"
        logger.info("[TEST] test_regular_login passed successfully")

    # Test auth - test login - 02
    # Verify Login failure with Incorrect Password
    def test_login_with_invalid_password(self, login_page, regular_user_account):
        """ Test login and verify user is logged in. """
        login_page.login(
            email=regular_user_account["email"],
            password="wrong_password123"
        )

        assert not login_page.is_logged_in(), "Login verification failed: User is logged in"

    # Class-level fixtures for security testing
    @pytest.fixture(scope="function")
    def sql_injection_payload(self):
        """SQL injection payload for security testing."""
        return "' OR 1=1 --"

    # Test auth - test login - 03
    # Verify Login page is secure against SQL Injection.
    def test_sql_injection_protection(self, login_page, sql_injection_payload):
        """ Test login and verify user is logged in. """
        login_page.login(
            email=sql_injection_payload,
            password="123456"
        )

        assert not login_page.is_logged_in(), "Login verification failed: User is logged in"
