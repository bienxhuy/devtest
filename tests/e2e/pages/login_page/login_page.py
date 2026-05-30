from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from tests.e2e.pages.login_page.login_page_locators import LoginPageLocators as LgLocators
from core.utils.base_page import BasePage
from core.utils.logs import get_logger


logger = get_logger()


class LoginPage(BasePage):
    def __init__(self, driver, base_url):
        super().__init__(driver, base_url)
        self.open_page()

    def open_page(self):
        self.open(self.base_url + "/login")

    def login(self, email, password):
        self.fill(LgLocators.LOGIN_EMAIL_INPUT, email, name="login email input")
        self.fill(LgLocators.LOGIN_PASSWORD_INPUT, password, name="login password input")
        self.click(LgLocators.LOGIN_BUTTON, name="login button")

    def register(self, name, email, password):
        self.fill(LgLocators.REGISTER_NAME_INPUT, name, name="register name input")
        self.fill(LgLocators.REGISTER_EMAIL_INPUT, email, name="register email input")
        self.fill(LgLocators.REGISTER_PASSWORD_INPUT, password, name="register password input")
        self.click(LgLocators.REGISTER_BUTTON, name="register button")

    def switch_mode(self):
        self.click(LgLocators.SWITCH_LOGIN_REGISTER_BUTTON, name="switch mode button")

    def get_login_error(self):
        return self.get_text(LgLocators.LOGIN_ERROR_MESSAGE, name="login error message")

    def get_register_error(self):
        return self.get_text(LgLocators.REGISTER_ERROR_MESSAGE, name="register error message")

    def is_logged_in(self):
        try:
            WebDriverWait(self.driver, 10).until(
                lambda d: "/login" not in d.current_url
            )
            return True
        except TimeoutException:
            logger.warning(f"[LOGIN_PAGE] Still on login URL: {self.driver.current_url}")
            return False
