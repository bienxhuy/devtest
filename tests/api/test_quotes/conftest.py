import pytest
from core.utils.api_client import APIClient
from tests.api.helpers.auth import register_and_login
from tests.api.mock_data.quotes import QuotePayloadBuilder


@pytest.fixture
def other_user_client():
    _, token = register_and_login()
    return APIClient(token=token)
