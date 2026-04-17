from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from core.logs.logger import get_logger
from dotenv import load_dotenv
import os


# Create a logger to log error
logger = get_logger()
# Load environment variables from .env file
load_dotenv()


# BasePage class
class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.BASE_URL = os.getenv("BASE_URL")

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

    # This method safely sends keys to an element, waiting for it to be present
    def send_keys(self, locator, text, success_message="", element="element", timeout=10):
        if not locator:
            return f"No locator for '{element}'"

        try:
            element_object = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((By.XPATH, locator))
            )
            element_object.clear()
            element_object.send_keys(text)
            return success_message

        except TimeoutException:
            logger.error(f"[BASE_PAGE] Timeout while "
                         f"waiting for {element} to be present")
            return (f"Timeout while waiting for "
                    f"'{element}' to be present")

        except Exception as e:
            logger.error(f"[BASE_PAGE] Error sending keys to {element}: {e}")
            return (f"Error sending keys to '{element}'")

    # This method safely retrieves the inner text of an element, waiting for it to be present
    def get_inner_text(self, locator, element="element", timeout=10):
        if not locator:
            return f"No locator for '{element}'"

        try:
            element_object = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((By.XPATH, locator))
            )
            return element_object.text

        except TimeoutException:
            logger.error(f"[BASE_PAGE] Timeout while "
                         f"waiting for {element} to be present")
            return (f"Timeout while waiting for "
                    f"'{element}' to be present")

        except Exception as e:
            logger.error(f"[BASE_PAGE] Error getting text of {element}: {e}")
            return (f"Error getting text of '{element}'")

     # This method navigates to a specified URL
    def go_to_url(self, url):
        try:
            self.driver.get(url)
            return f"Navigated to URL: {url}"
        except Exception as e:
            logger.error(f"[BASE_PAGE] Error navigating to URL {url}: {e}")
            return f"Error navigating to URL: {url}"
