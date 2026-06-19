import pytest
from tests.api.helpers.api_endpoints import APIEndpoints


@pytest.mark.api
@pytest.mark.smoke
def test_logout_all_with_valid_token_returns_204(cookie_jar):
    client = cookie_jar
    res = client.post(APIEndpoints.logout_all)
    assert res.status_code == 204


@pytest.mark.api
@pytest.mark.regression
def test_logout_all_without_token_returns_401(api_client):
    res = api_client.post(APIEndpoints.logout_all)
    assert res.status_code == 401


@pytest.mark.api
@pytest.mark.regression
def test_logout_all_invalidates_refresh_token(cookie_jar):
    client = cookie_jar
    refresh_cookie = client.session.cookies.get("refreshToken")
    assert refresh_cookie is not None
    
    res1 = client.post(APIEndpoints.logout_all)
    assert res1.status_code == 204
    
    # Attempt to refresh with the old token, which should now be invalid
    res = client.post(
        APIEndpoints.refresh,
        cookies={"refreshToken": refresh_cookie},
    )
    assert res.status_code == 401
