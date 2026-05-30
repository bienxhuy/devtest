import json
import uuid
import pytest
from pathlib import Path

from tests.e2e.pages.login_page.login_page import LoginPage
from tests.e2e.pages.home_page.home_page import HomePage
from tests.e2e.pages.quote_page.quote_page import QuotePage


def _load_test_data() -> dict:
    data_path = Path(__file__).resolve().parents[1] / "mock_data" / "env_config.json"
    with data_path.open("r", encoding="utf-8") as config_file:
        return json.load(config_file)
    

def get_random_string(length=8):
    return uuid.uuid4().hex[:length]


# Page object fixtures
@pytest.fixture
def login_page(driver, base_url):
    return LoginPage(driver, base_url)


@pytest.fixture
def home_page(driver, base_url):
    return HomePage(driver, base_url)


@pytest.fixture
def quote_page(driver, base_url):
    return QuotePage(driver, base_url)


# Data fixtures
@pytest.fixture(scope="session")
def test_data():
    return _load_test_data()


@pytest.fixture(scope="session")
def regular_user_account(test_data):
    return test_data["accounts"]["regular_user"]


@pytest.fixture
def new_user(test_data):
    base = test_data["new_user"]
    return {
        "name": base["name"],
        "email": f"newuser_{get_random_string(8)}@example.com",
        "password": base["password"]
    }


@pytest.fixture(scope="session")
def sample_quote(test_data):
    return test_data["quotes"]["sample"] + f" {get_random_string(6)}"


@pytest.fixture(scope="session")
def second_quote(test_data):
    return test_data["quotes"]["second"] + f" {get_random_string(6)}"