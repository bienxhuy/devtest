import pytest
from tests.api.helpers.assertions import assert_auth_response
from tests.api.mock_data.users import UserPayloadBuilder
from tests.api.helpers.api_endpoints import APIEndpoints


@pytest.mark.api
@pytest.mark.smoke
def test_register_with_valid_data_returns_201(api_client, fresh_user):    
    res = api_client.post(APIEndpoints.register, json=fresh_user)
    assert res.status_code == 201
    body = res.json()
    assert_auth_response(body)
    assert body["data"]["user"]["email"] == fresh_user["email"]
    set_cookie = res.headers.get("Set-Cookie", "")
    assert "refreshToken" in set_cookie


@pytest.mark.api
@pytest.mark.regression
def test_register_with_existing_email_returns_409(api_client, fresh_user):
    res1 = api_client.post(APIEndpoints.register, json=fresh_user)
    assert res1.status_code in (200, 201)
    res2 = api_client.post(APIEndpoints.register, json=fresh_user)
    assert res2.status_code == 409


@pytest.mark.api
@pytest.mark.regression
def test_register_without_name_returns_400(api_client, fresh_user):
    fresh_user.pop("name", None)
    res = api_client.post(APIEndpoints.register, json=fresh_user)
    assert res.status_code == 400


@pytest.mark.api
@pytest.mark.regression
def test_register_without_email_returns_400(api_client, fresh_user):
    fresh_user.pop("email", None)
    res = api_client.post(APIEndpoints.register, json=fresh_user)
    assert res.status_code == 400


@pytest.mark.api
@pytest.mark.regression
def test_register_without_password_returns_400(api_client, fresh_user):
    fresh_user.pop("password", None)
    res = api_client.post(APIEndpoints.register, json=fresh_user)
    assert res.status_code == 400


@pytest.mark.api
@pytest.mark.regression
def test_register_with_short_password_returns_400(api_client):
    payload = UserPayloadBuilder().with_password("123").build()
    res = api_client.post(APIEndpoints.register, json=payload)
    assert res.status_code == 400


@pytest.mark.api
@pytest.mark.security
def test_register_response_does_not_expose_password(api_client, fresh_user):
    res = api_client.post(APIEndpoints.register, json=fresh_user)
    assert res.status_code in (200, 201)
    body = res.json()
    user = body["data"]["user"]
    assert "password" not in user
    assert "hash" not in user


@pytest.mark.api
@pytest.mark.security
def test_register_with_sql_injection_in_email_returns_400_or_409(api_client):
    payload = UserPayloadBuilder().with_email("test'; DROP TABLE users;").build()
    res = api_client.post(APIEndpoints.register, json=payload)
    assert res.status_code in (400, 409)
