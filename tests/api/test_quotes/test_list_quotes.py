import pytest
from tests.api.helpers.assertions import assert_quote_shape
from tests.api.helpers.api_endpoints import APIEndpoints


@pytest.mark.api
@pytest.mark.smoke
def test_get_quotes_returns_200(api_client):
    res = api_client.get(APIEndpoints.quotes)
    assert res.status_code == 200
    body = res.json()
    assert "data" in body
    assert "quotes" in body["data"]
    assert isinstance(body["data"]["quotes"], list)


@pytest.mark.api
@pytest.mark.regression
def test_get_quotes_default_pagination(api_client):
    res = api_client.get(APIEndpoints.quotes)
    assert res.status_code == 200
    body = res.json()
    pag = body["data"].get("pagination", {})
    assert pag.get("page", 1) == 1
    assert pag.get("limit", 10) == 10


@pytest.mark.api
@pytest.mark.regression
def test_get_quotes_with_custom_page_and_limit(api_client):
    res = api_client.get(APIEndpoints.quotes, params={"page": 2, "limit": 5})
    assert res.status_code == 200
    body = res.json()
    pag = body["data"].get("pagination", {})
    assert pag.get("page") == 2
    assert pag.get("limit") == 5


@pytest.mark.api
@pytest.mark.regression
def test_get_quotes_with_invalid_page_returns_400(api_client):
    res = api_client.get(APIEndpoints.quotes, params={"page": 0})
    assert res.status_code == 400


@pytest.mark.api
@pytest.mark.regression
def test_get_quotes_with_invalid_limit_returns_400(api_client):
    res = api_client.get(APIEndpoints.quotes, params={"limit": 0})
    assert res.status_code == 400


@pytest.mark.api
@pytest.mark.regression
def test_get_quotes_with_limit_exceeding_max_returns_400(api_client):
    res = api_client.get(APIEndpoints.quotes, params={"limit": 101})
    assert res.status_code == 400


@pytest.mark.api
@pytest.mark.security
def test_get_quotes_does_not_require_auth(api_client):
    res = api_client.get(APIEndpoints.quotes)
    assert res.status_code == 200


@pytest.mark.api
@pytest.mark.regression
def test_quote_object_shape(api_client):
    res = api_client.get(APIEndpoints.quotes)
    assert res.status_code == 200
    body = res.json()
    quotes = body["data"].get("quotes", [])
    if quotes:
        assert_quote_shape(quotes[0])
