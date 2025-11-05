from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from logs.logger import get_logger


# Create a logger to log error
logger = get_logger()


# BasePage class    
class BasePage: 
    def __init__(self, driver):
        self.driver = driver

    # This method safely clicks an element, waiting for it to be clickable
    def safe_click(self, locator, success_message, element="element", timeout=10):
        if not locator:
            return f"No locator for '{element}'"

        # Wait for the element to be clickable and click it
        try:
            element_object = WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable((By.XPATH, locator))
            )
            element_object.click()
            return success_message

        except TimeoutException:
            logger.error(f"[BASE_PAGE] Timeout while " 
                         f"waiting for {element} to be clickable")
            return (f"Timeout while waiting for "
                    f"'{element}' to be clickable")

        except Exception as e:
            logger.error(f"[BASE_PAGE] Error clicking {element}: {e}")
            return (f"Error clicking '{element}'")
