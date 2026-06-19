import pytest
from tests.api.helpers.api_endpoints import APIEndpoints


@pytest.mark.api
@pytest.mark.smoke
def test_logout_with_cookie_returns_204(cookie_jar):
    client = cookie_jar
    res = client.post(APIEndpoints.logout)
    assert res.status_code == 204
    set_cookie = res.headers.get("Set-Cookie", "")
    assert "refreshToken" in set_cookie and ("Expires" in set_cookie or "expires" in set_cookie)


@pytest.mark.api
@pytest.mark.regression
def test_logout_without_cookie_returns_204(api_client):
    res = api_client.post(APIEndpoints.logout)
    assert res.status_code == 204
