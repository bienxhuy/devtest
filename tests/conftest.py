import pytest
from dotenv import load_dotenv
from selenium import webdriver

# This is a pytest fixture that initializes a browser instance for testing
# Provides a browser instance to the tests
@pytest.fixture(scope="session")
def browser():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    yield driver
    driver.quit()
