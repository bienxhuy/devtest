from core.utils.api_client import APIClient
from tests.api.mock_data.users import UserPayloadBuilder
from tests.api.helpers.api_endpoints import APIEndpoints


def register_and_login():
    """This helper registers a new user and logs in to get a valid token.
    Returns (payload, token) for the new user."""
    client = APIClient()
    payload = UserPayloadBuilder().build()
    client.post(APIEndpoints.register, json=payload)
    res = client.post(APIEndpoints.login, json={
        "email": payload["email"],
        "password": payload["password"],
    })
    res.raise_for_status()
    token = res.json()["data"]["accessToken"]
    return payload, token


# if __name__ == "__main__":
#     user_info, access_token = register_and_login()
#     print("Registered user:", user_info)
#     print("Access token:", access_token)
    