from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

class BasePage:
    def __init__(self, driver):
        self.driver = driver # Store the WebDriver instance for use in other methods
    
    # This method tries to find an element by using XPath
    # TODO: Fix the method to capture screenshot the element when it fails
    def get_element(self, locator):
        try:
            element = self.driver.find_element(By.XPATH, locator)
            return element
        except NoSuchElementException:
            print(f"No elements found for locator: {locator}")
            return None

    # base_page.py
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

class BasePage:
    def __init__(self, driver):
        self.driver = driver

    # This method safely clicks an element, waiting for it to be clickable
    # TODO: Add ultility methods: safe_send_keys, safe_get_element_text
    # is_element_visible
    def safe_click(self, locator, description="element", fallback_message=None, timeout=10):
        if not locator:
            print(fallback_message or f"[safe_click] No locator provided for '{description}'")
            return

        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable(locator)
            )
            element.click()
            print(f"[safe_click] Clicked on '{description}'")
        except TimeoutException:
            print(f"[safe_click] Timeout: Could not find clickable '{description}'")
        except Exception as e:
            print(f"[safe_click] Error clicking '{description}': {e}")
