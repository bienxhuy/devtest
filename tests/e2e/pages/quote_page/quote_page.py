from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tests.e2e.pages.quote_page.quote_page_locators import QuotePageLocators as QpLocators
from core.utils.base_page import BasePage
from core.utils.logs import get_logger


logger = get_logger()


class QuotePage(BasePage):
    def __init__(self, driver, base_url):
        super().__init__(driver, base_url)

    def open_page(self):
        self.open(self.base_url + "/quotes")

    def get_first_quote_text(self):
        return self.get_text(QpLocators.FIRST_QUOTE_TEXT, name="first quote text")

    def create_quote(self, text):
        logger.info(f"[QUOTE_PAGE] Creating quote: '{text}'")
        self.click(QpLocators.NEW_QUOTE_BUTTON, name="new quote button")
        self.fill(QpLocators.QUOTE_TEXT_INPUT, text, name="quote text input")
        self.click(QpLocators.POST_QUOTE_BUTTON, name="post quote button")
        self._wait_for(EC.invisibility_of_element_located(QpLocators.QUOTE_TEXT_INPUT), name="create quote modal")
        self.click(QpLocators.REFRESH_BUTTON, name="refresh button")
        WebDriverWait(self.driver, 10).until(lambda d: text in self.get_first_quote_text())

    # Delete
    def delete_first_own_quote(self):
        logger.info("[QUOTE_PAGE] Deleting first owned quote")
        self.click(QpLocators.FIRST_OWN_QUOTE_DELETE_BUTTON, name="delete button")
        self.click(QpLocators.CONFIRM_DELETE_BUTTON, name="confirm delete button")
