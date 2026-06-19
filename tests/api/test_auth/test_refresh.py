import pytest
from tests.api.helpers.assertions import assert_auth_response
from tests.api.helpers.api_endpoints import APIEndpoints


@pytest.mark.api
@pytest.mark.smoke
def test_refresh_with_valid_cookie_returns_200(cookie_jar):
    client = cookie_jar
    old_token = client.get_token()
    res = client.post(APIEndpoints.refresh)
    assert res.status_code == 200
    body = res.json()
    assert_auth_response(body)
    new_token = body["data"]["accessToken"]
    assert new_token != old_token


@pytest.mark.api
@pytest.mark.regression
def test_refresh_without_cookie_returns_401(api_client):
    res = api_client.post(APIEndpoints.refresh)
    assert res.status_code == 401


@pytest.mark.api
@pytest.mark.security
def test_refresh_with_tampered_cookie_returns_401(cookie_jar):
    client = cookie_jar
    # Overwrite any existing refresh token cookie and set a tampered one
    client.session.cookies.set(
        "refreshToken",
        "tampered.token.value",
        domain="localhost.local",
        path=APIEndpoints.refresh,
    )
    res = client.post(APIEndpoints.refresh)
    assert res.status_code == 401
