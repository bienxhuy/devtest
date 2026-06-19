import pytest
from tests.api.helpers.api_endpoints import APIEndpoints


@pytest.mark.api
@pytest.mark.smoke
def test_delete_own_quote_returns_204(auth_client):
    # create quote
    res = auth_client.post(APIEndpoints.quotes, json={"text": "to delete"})
    assert res.status_code == 201
    quote_id = res.json()["data"]["id"]
    delete_res = auth_client.delete(APIEndpoints.quotes, json={"id": quote_id})
    assert delete_res.status_code == 204


@pytest.mark.api
@pytest.mark.regression
def test_delete_quote_without_auth_returns_401(api_client):
    res = api_client.delete(APIEndpoints.quotes, json={"id": 1})
    assert res.status_code == 401


@pytest.mark.api
@pytest.mark.regression
def test_delete_nonexistent_quote_returns_404(auth_client):
    res = auth_client.delete(APIEndpoints.quotes, json={"id": 99999999})
    assert res.status_code == 404


@pytest.mark.api
@pytest.mark.regression
def test_delete_with_invalid_id_type_returns_400(auth_client):
    res = auth_client.delete(APIEndpoints.quotes, json={"id": "not-an-int"})
    assert res.status_code == 400


@pytest.mark.api
@pytest.mark.regression
def test_delete_quote_missing_id_returns_400(auth_client):
    res = auth_client.delete(APIEndpoints.quotes, json={})
    assert res.status_code == 400


@pytest.mark.api
@pytest.mark.security
def test_delete_another_users_quote_returns_403(auth_client, other_user_client):
    # User A creates
    res = auth_client.post(APIEndpoints.quotes, json={"text": "private"})
    assert res.status_code == 201
    quote_id = res.json()["data"]["id"]
    # User B tries to delete
    delete_res = other_user_client.delete(APIEndpoints.quotes, json={"id": quote_id})
    assert delete_res.status_code == 403
    # cleanup by owner
    auth_client.delete(APIEndpoints.quotes, json={"id": quote_id})
    