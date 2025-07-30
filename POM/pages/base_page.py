import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from datetime import datetime

from logs.logger import get_logger 

# Use module-specific logger
logger = get_logger(__name__)

SCREENSHOT_DIR = "../utils/screenshots"

# BasePage class    
class BasePage: 
    def __init__(self, driver):
        self.driver = driver

    # This method safely clicks an element, waiting for it to be clickable
    # TODO: Add ultility methods: safe_send_keys, safe_get_element_text
    # is_element_visible
    def safe_click(self, locator, description="element",
               fallback_message=None, timeout=10):
        if not locator:
            message = (fallback_message or
                    f"[safe_click] No locator for '{description}'")
            logger.warning(message)
            self.take_screenshot(description)
            return

        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable((By.XPATH,locator))
            )
            element.click()
            logger.info(f"[safe_click] Clicked on '{description}'")
            return True

        except TimeoutException:
            logger.error(
                f"[safe_click] Timeout while waiting for "
                f"'{description}' to be clickable"
            )
            self.take_screenshot(description)

        except Exception as e:
            logger.error(
                f"[safe_click] Error clicking on '{description}': {e}"
            )
            self.take_screenshot(description)
            
        return False

            
    # This method takes a screenshot and saves it with a timestamp
    def take_screenshot(self, name = "error"):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{name.replace(' ', '_')}_{timestamp}.png"
        filepath = os.path.join(SCREENSHOT_DIR, filename)
        try:
            self.driver.save_screenshot(filepath)
            logger.info(f"[safe_click] Screenshot saved to: {filepath}")
        except Exception as e:
            logger.info(f"[safe_click] Failed to take screenshot: {e}")
