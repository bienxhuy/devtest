import pytest
from core.utils.api_client import APIClient
from core.utils.logs import get_logger
from tests.api.helpers.auth import register_and_login
from tests.api.mock_data.quotes import QuotePayloadBuilder


logger = get_logger()


@pytest.fixture
def other_user_client():
    logger.info("[API_FIXTURES] Creating authenticated client for a second user")
    _, token = register_and_login()
    return APIClient(token=token)
