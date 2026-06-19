import pytest
from tests.api.helpers.assertions import assert_auth_response
from tests.api.helpers.api_endpoints import APIEndpoints


@pytest.mark.api
@pytest.mark.smoke
def test_login_with_valid_credentials_returns_200(registered_user, api_client):
    payload, _ = registered_user
    res = api_client.post(APIEndpoints.login, json={
        "email": payload["email"],
        "password": payload["password"],
    })
    assert res.status_code == 200
    body = res.json()
    assert_auth_response(body)


@pytest.mark.api
@pytest.mark.regression
def test_login_with_wrong_password_returns_401(registered_user, api_client):
    payload, _ = registered_user
    res = api_client.post(APIEndpoints.login, json={
        "email": payload["email"],
        "password": "wrong-password",
    })
    assert res.status_code == 401


@pytest.mark.api
@pytest.mark.regression
def test_login_with_nonexistent_email_returns_401(api_client):
    res = api_client.post(APIEndpoints.login, json={
        "email": "noone@example.test",
        "password": "whatever",
    })
    assert res.status_code == 401


@pytest.mark.api
@pytest.mark.regression
def test_login_without_email_returns_400(api_client):
    res = api_client.post(APIEndpoints.login, json={"password": "x"})
    assert res.status_code == 400


@pytest.mark.api
@pytest.mark.regression
def test_login_without_password_returns_400(api_client):
    res = api_client.post(APIEndpoints.login, json={"email": "a@b.c"})
    assert res.status_code == 400


@pytest.mark.api
@pytest.mark.regression
def test_login_sets_httponly_refresh_token_cookie(registered_user, api_client):
    payload, _ = registered_user
    res = api_client.post(APIEndpoints.login, json={
        "email": payload["email"],
        "password": payload["password"],
    })
    assert res.status_code == 200
    set_cookie = res.headers.get("Set-Cookie", "")
    assert "HttpOnly" in set_cookie or "httponly" in set_cookie


@pytest.mark.api
@pytest.mark.security
def test_login_with_sql_injection_in_email_returns_401(registered_user, api_client):
    payload, _ = registered_user
    res = api_client.post(APIEndpoints.login, json={
        "email": payload["email"] + "' OR 1=1;--",
        "password": payload["password"],
    })
    assert res.status_code == 401


@pytest.mark.api
@pytest.mark.security
def test_login_with_sql_injection_in_password_returns_401(registered_user, api_client):
    payload, _ = registered_user
    res = api_client.post(APIEndpoints.login, json={
        "email": payload["email"],
        "password": "' OR '1'='1",
    })
    assert res.status_code == 401


@pytest.mark.api
@pytest.mark.security
def test_login_response_does_not_expose_password_hash(registered_user, api_client):
    payload, _ = registered_user
    res = api_client.post(APIEndpoints.login, json={
        "email": payload["email"],
        "password": payload["password"],
    })
    assert res.status_code == 200
    body = res.json()
    assert "password" not in body["data"]["user"]
