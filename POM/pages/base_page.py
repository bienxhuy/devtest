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
            return element

