from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from tests.e2e.pages.home_page.home_page_locators import HomePageLocators as HpLocators
from core.utils.base_page import BasePage
from core.utils.logs import get_logger


logger = get_logger()


class HomePage(BasePage):
    def __init__(self, driver, base_url):
        super().__init__(driver, base_url)
        self.open_page()

    def open_page(self):
        self.open(self.base_url)

    def go_to_login(self):
        self.click(HpLocators.LOGIN_BUTTON, name="login button")

    def logout(self):
        self.click(HpLocators.LOGOUT_BUTTON, name="logout button")

    def go_to_quotes(self):
        self.click(HpLocators.QUOTE_PAGE_BUTTON, name="quote page button")

    def get_logged_out_hero_text(self):
        return self.get_text(HpLocators.LOGGED_OUT_HERO, name="logged out hero text")

    def get_logged_in_hero_text(self):
        return self.get_text(HpLocators.LOGGED_IN_HERO, name="logged in hero text")

    def is_logged_out(self):
        button_text = self.get_text(HpLocators.LOGIN_BUTTON, name="auth button")
        button_text = button_text.strip().lower()
        return button_text == "login"
