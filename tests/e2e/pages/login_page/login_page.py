from tests.e2e.pages.login_page.login_page_locators import Login_PageLocators as LgLocators
from tests.e2e.pages.login_page.login_page_notifications import LoginPageNotifications as LgNoti
from core.base_page import BasePage
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException


class LoginPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.go_to_url(self.BASE_URL + "/login")
    
    # Login action - returns notification message
    def login(self, email, password):
        self.send_keys(LgLocators.LOGIN_EMAIL_INPUT, email, "", "Login Email Input")
        self.send_keys(LgLocators.LOGIN_PASSWORD_INPUT, password, "", "Login Password Input")
        return self.safe_click(LgLocators.LOGIN_BUTTON, LgNoti.LOGIN_BUTTON_CLICKED_SUCCESS, "Login Button")
    
    # Register action - returns notification message
    def register(self, name, email, password):
        self.send_keys(LgLocators.REGISTER_NAME_INPUT, name, "", "Register Name Input")
        self.send_keys(LgLocators.REGISTER_EMAIL_INPUT, email, "", "Register Email Input")
        self.send_keys(LgLocators.REGISTER_PASSWORD_INPUT, password, "", "Register Password Input")
        return self.safe_click(LgLocators.REGISTER_BUTTON, LgNoti.REGISTER_BUTTON_CLICKED_SUCCESS, "Register Button")
        
    # Check if login was successful
    def is_logged_in(self):
        from core.utils.logs import get_logger
        logger = get_logger()
        # In SPA flows, redirect can happen after click without a full page reload.
        try:
            WebDriverWait(self.driver, 10).until(
                lambda d: "/login" not in d.current_url
            )
        except TimeoutException:
            logger.warning(f"[LOGIN_PAGE] Login check timed out, still on URL: {self.driver.current_url}")
            return False
        return True
