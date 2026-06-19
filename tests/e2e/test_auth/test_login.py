import pytest
from core.utils.logs import get_logger


logger = get_logger()


# EA-01
@pytest.mark.e2e
@pytest.mark.regression
def test_regular_login(login_page, regular_user_account):
    logger.info("[TEST] EA-01 test_regular_login starts")
    login_page.open_page()
    login_page.login(
        email=regular_user_account["email"],
        password=regular_user_account["password"]
    )
    assert login_page.is_logged_in(), (
        "User should be redirected away from /login after valid login"
    )
    logger.info("[TEST] EA-01 passed")

# EA-02
@pytest.mark.e2e
@pytest.mark.regression
def test_register_new_user(login_page, new_user):
    logger.info("[TEST] EA-02 test_register_new_user starts")
    login_page.open_page()
    login_page.switch_mode()
    login_page.register(
        name=new_user["name"],
        email=new_user["email"],
        password=new_user["password"]
    )
    assert login_page.is_logged_in(), (
        "User should be auto-logged in immediately after registration"
    )
    logger.info("[TEST] EA-02 passed")

# EA-03
@pytest.mark.e2e
@pytest.mark.regression
def test_login_invalid_password(login_page, regular_user_account):
    logger.info("[TEST] EA-03 test_login_invalid_password starts")
    login_page.open_page()
    login_page.login(
        email=regular_user_account["email"],
        password="WrongPassword999!"
    )
    assert not login_page.is_logged_in(), (
        "User should remain on /login when password is incorrect"
    )
    logger.info("[TEST] EA-03 passed")

# EA-04
@pytest.mark.e2e
@pytest.mark.regression
def test_logout(home_page, login_page, regular_user_account):
    logger.info("[TEST] EA-04 test_logout starts")
    login_page.open_page()
    login_page.login(
        email=regular_user_account["email"],
        password=regular_user_account["password"]
    )
    assert login_page.is_logged_in(), "Pre-condition: user must be logged in"
    home_page.logout()
    assert home_page.is_logged_out(), (
        "Home page should return to guest state after logout"
    )
    logger.info("[TEST] EA-04 passed")

# EA-05
@pytest.mark.e2e
@pytest.mark.regression
def test_home_page_logged_in_state(home_page, login_page, regular_user_account):
    logger.info("[TEST] EA-05 test_home_page_logged_in_state starts")
    login_page.open_page()
    login_page.login(
        email=regular_user_account["email"],
        password=regular_user_account["password"]
    )
    assert login_page.is_logged_in(), "Pre-condition: user must be logged in"
    hero_text = home_page.get_logged_in_hero_text()
    assert regular_user_account["name"] in hero_text, (
        "Hero text should contain user's name "
        f"'{regular_user_account['name']}', got: '{hero_text}'"
    )
    logger.info("[TEST] EA-05 passed")
