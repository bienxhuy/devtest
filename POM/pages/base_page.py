from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from logs.logger import get_logger


# Get a logger instance for logging within the page objects
logger = get_logger()


# BasePage class    
class BasePage: 
    def __init__(self, driver):
        self.driver = driver

    # This method safely clicks an element, waiting for it to be clickable
    # TODO: Add ultility methods: safe_send_keys, safe_get_element_text
    # is_element_visible
    def safe_click(self, locator, success_message, element="element", timeout=10):
        if not locator:
            logger.error(f"[safe_click] No locator for '{element}'")
            return f"[safe_click] No locator for '{element}'"

        # Wait for the element to be clickable and click it
        try:
            logger.info(f"[safe_click] Waiting for '{element}' to be clickable")
            element = WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable((By.XPATH, locator))
            )
            element.click()
            logger.info(f"[safe_click] Clicked '{element}' successfully")
            return success_message

        except TimeoutException:
            logger.error(f"[safe_click] Timeout while waiting for '{element}' to be clickable")
            return (f"Timeout while waiting for "
                    f"'{element}' to be clickable")

        except Exception as e:
            logger.error(f"[safe_click] Error clicking '{element}': {str(e)}")
            return (f"Error clicking '{element}'")
