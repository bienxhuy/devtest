import pytest
import sys
import os
from selenium import webdriver


# Go up one directory to include dev_test in sys.path
# This allows the tests (files) to import modules from the dev_test package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


# This is a pytest fixture that initializes a driver instance for testing
# Provides a driver instance to the tests
@pytest.fixture(scope="session")
def driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    yield driver
    driver.quit()
