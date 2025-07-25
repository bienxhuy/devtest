import os
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from datetime import datetime

SCREENSHOT_DIR = "../utils/screenshots"

class BasePage:
    def __init__(self, driver):
        self.driver = driver

    # This method safely clicks an element, waiting for it to be clickable
    # TODO: Add ultility methods: safe_send_keys, safe_get_element_text
    # is_element_visible
    def safe_click(self, locator, description="element",
               fallback_message=None, timeout=10):
        if not locator:
            print(fallback_message or
                f"[safe_click] No locator for '{description}'")
            return

        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable(locator)
            )
            element.click()
            print(f"[safe_click] Clicked on '{description}'")
        except TimeoutException:
            print(f"[safe_click] Timeout: '{description}' not clickable")
            self._take_screenshot(description)
        except Exception as e:
            print(f"[safe_click] Error clicking '{description}': {e}")
            self._take_screenshot(description)

    # This method takes a screenshot and saves it with a timestamp
    def take_screenshot(self, name = "error"):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{name.replace(' ', '_')}_{timestamp}.png"
        filepath = os.path.join(SCREENSHOT_DIR, filename)
        try:
            self.driver.save_screenshot(filepath)
            print(f"[safe_click] Screenshot saved to: {filepath}")
        except Exception as e:
            print(f"[safe_click] Failed to take screenshot: {e}")
