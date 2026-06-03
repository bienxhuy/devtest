from core.utils.api_client import APIClient
from core.utils.logs import get_logger
from tests.api.mock_data.users import UserPayloadBuilder
from tests.api.helpers.api_endpoints import APIEndpoints


logger = get_logger()


def register_and_login(base_url):
    """This helper registers a new user and logs in to get a valid token.
    Returns (payload, token) for the new user."""
    logger.info("[API_AUTH] Registering a fresh user and requesting access token")
    client = APIClient(base_url=base_url)
    payload = UserPayloadBuilder().build()
    register_res = client.post(APIEndpoints.register, json=payload)
    logger.debug(f"[API_AUTH] Register response -> {register_res.status_code}")
    register_res.raise_for_status()
    res = client.post(APIEndpoints.login, json={
        "email": payload["email"],
        "password": payload["password"],
    })
    logger.debug(f"[API_AUTH] Login response -> {res.status_code}")
    res.raise_for_status()
    token = res.json()["data"]["accessToken"]
    logger.info("[API_AUTH] Fresh user authenticated successfully")
    return payload, token
