import pytest
from POM.login_page.login_page import LoginPage


# Page object fixtures - return initialized page objects
@pytest.fixture
def login_page(driver):
    """Returns initialized LoginPage. Use when you need a fresh login page."""
    return LoginPage(driver)
  

# Account fixtures
@pytest.fixture(scope="session")
def regular_user_account():
    """Provides a valid student account for testing."""
    return {
        "email": "bxh@gmail.com",
        "password": "Huy123456",
        "name": "Bien Xuan Huy"
    }