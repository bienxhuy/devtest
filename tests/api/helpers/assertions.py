def assert_auth_response(body):
    assert "status" in body
    assert "data" in body
    assert "accessToken" in body["data"]
    assert isinstance(body["data"]["accessToken"], str)
    assert len(body["data"]["accessToken"]) > 0
    user = body["data"]["user"]
    assert "id" in user
    assert "name" in user
    assert "email" in user
    assert "role" in user


def assert_quote_shape(quote):
    assert "id" in quote
    assert "text" in quote
    assert "owner" in quote
    assert "createdAt" in quote
    assert "updatedAt" in quote
    owner = quote["owner"]
    assert "id" in owner
    assert "email" in owner
