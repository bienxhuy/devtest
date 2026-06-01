import pytest
from core.utils.logs import get_logger


logger = get_logger()


@pytest.fixture
def login_and_go_to_quotes(login_page, quote_page, regular_user_account):
    """Logs in with the provided account and navigates to the quote page."""
    account = regular_user_account
    login_page.open_page()
    login_page.login(email=account["email"], password=account["password"])
    assert login_page.is_logged_in(), "Pre-condition: user must be logged in"
    quote_page.open_page()

# EA-06
@pytest.mark.e2e
@pytest.mark.regression
@pytest.mark.xdist_group(name="quote_tests")
def test_view_public_quotes(login_and_go_to_quotes, home_page, quote_page, sample_quote):
    logger.info("[TEST] EA-06 test_view_public_quotes starts")
    # Reopen because home_page fixture automatically navigates to home after initiation
    quote_page.open_page()
    quote_page.create_quote(sample_quote)
    
    home_page.open_page()
    home_page.logout()
    assert home_page.is_logged_out(), "Pre-condition: must be logged out before guest check"
    
    quote_page.open_page()
    first_quote = quote_page.get_first_quote_text()
    assert first_quote, "At least one quote should be visible to a guest user"
    logger.info("[TEST] EA-06 passed")

# EA-07
@pytest.mark.e2e
@pytest.mark.regression
@pytest.mark.xdist_group(name="quote_tests")
def test_create_quote(login_and_go_to_quotes, quote_page, sample_quote):
    logger.info("[TEST] EA-07 test_create_quote starts")
    quote_page.create_quote(sample_quote)
    first_quote = quote_page.get_first_quote_text()
    assert sample_quote in first_quote, (
        f"Newly created quote should appear at top of list. Got: '{first_quote}'"
    )
    logger.info("[TEST] EA-07 passed")

# EA-08
@pytest.mark.e2e
@pytest.mark.regression
@pytest.mark.xdist_group(name="quote_tests")
def test_delete_own_quote(login_and_go_to_quotes, quote_page, second_quote):
    logger.info("[TEST] EA-08 test_delete_own_quote starts")
    quote_page.create_quote(second_quote)

    created_text = quote_page.get_first_quote_text()
    assert second_quote in created_text, (
        "Pre-condition: created quote should be at top of list before deletion"
    )

    quote_page.delete_first_own_quote()
    remaining_text = quote_page.get_first_quote_text()
    assert second_quote not in remaining_text, (
        "Deleted quote should no longer appear in the list"
    )
    logger.info("[TEST] EA-08 passed")
