import pytest
from selenium import webdriver
from logs.logger import get_logger


# Get a logger instance for logging within the tests
logger = get_logger()


# This is a pytest fixture that initializes a driver instance for testing
# Provides a driver instance to the tests
@pytest.fixture(scope="session")
def driver():
    logger.info("[CONFTEST] - Initializing WebDriver instance for the test session.")
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")  # Required for Docker
    options.add_argument("--disable-dev-shm-usage")  # Avoids issues with shared memory in Docker
    options.add_argument("--disable-gpu")  # Disable GPU in headless mode
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    logger.info("[CONFTEST] - WebDriver instance initialized successfully.")
    yield driver
    logger.info("[CONFTEST] - Quitting WebDriver instance after the test session.")
    driver.quit()