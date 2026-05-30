from abc import ABC, abstractmethod
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from core.utils.logs import get_logger


logger = get_logger()


class BasePage(ABC):
    def __init__(self, driver, base_url):
        self.driver = driver
        self.base_url = base_url

    @abstractmethod
    def open_page(self):
        """Navigate to the page's base route."""
        raise NotImplementedError

    def _wait_for(self, condition, name="element", timeout=10):
        try:
            return WebDriverWait(self.driver, timeout).until(condition)
        except TimeoutException:
            logger.error(f"[BASE_PAGE] Timeout waiting for '{name}' ({timeout}s)")
            raise
        except Exception as e:
            logger.error(f"[BASE_PAGE] Unexpected error waiting for '{name}': {e}")
            raise

    def click(self, locator, name="element", timeout=10):
        self._wait_for(EC.element_to_be_clickable(locator), name, timeout).click()

    def fill(self, locator, text, name="element", timeout=10):
        element = self._wait_for(EC.element_to_be_clickable(locator), name, timeout)
        element.clear()
        element.send_keys(text)

    def get_text(self, locator, name="element", timeout=10):
        return self._wait_for(EC.visibility_of_element_located(locator), name, timeout).text

    def open(self, url):
        try:
            self.driver.get(url)
        except Exception as e:
            logger.error(f"[BASE_PAGE] Failed to navigate to '{url}': {e}")
            raise
