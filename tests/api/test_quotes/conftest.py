import pytest
from core.utils.api_client import APIClient
from core.utils.logs import get_logger
from tests.api.helpers.auth import register_and_login
from tests.api.mock_data.quotes import QuotePayloadBuilder


logger = get_logger()


@pytest.fixture
def other_user_client(base_url):
    logger.info("[API_FIXTURES] Creating authenticated client for a second user")
    _, token = register_and_login(base_url)
    return APIClient(base_url=base_url, token=token)
