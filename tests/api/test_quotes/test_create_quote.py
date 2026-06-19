import pytest
from tests.api.mock_data.quotes import QuotePayloadBuilder
from tests.api.helpers.api_endpoints import APIEndpoints


@pytest.mark.api
@pytest.mark.smoke
def test_create_quote_with_valid_data_returns_201(auth_client):
    res = auth_client.post(APIEndpoints.quotes, json=QuotePayloadBuilder().build())
    assert res.status_code == 201
    body = res.json()
    assert "data" in body and "id" in body["data"]


@pytest.mark.api
@pytest.mark.regression
def test_create_quote_without_auth_returns_401(api_client):
    res = api_client.post(APIEndpoints.quotes, json=QuotePayloadBuilder().build())
    assert res.status_code == 401


@pytest.mark.api
@pytest.mark.regression
def test_create_quote_without_text_returns_400(auth_client):
    res = auth_client.post(APIEndpoints.quotes, json={})
    assert res.status_code == 400


@pytest.mark.api
@pytest.mark.regression
def test_create_quote_with_empty_text_returns_400(auth_client):
    res = auth_client.post(APIEndpoints.quotes, json={"text": ""})
    assert res.status_code == 400


@pytest.mark.api
@pytest.mark.security
def test_create_quote_with_xss_payload_is_stored_as_plain_text(auth_client):
    payload = QuotePayloadBuilder().with_text("<script>alert(1)</script>").build()
    res = auth_client.post(APIEndpoints.quotes, json=payload)
    assert res.status_code == 201
    body = res.json()
    assert body["data"]["text"] == payload["text"]
