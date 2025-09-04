import pytest
from selenium import webdriver


# This is a pytest fixture that initializes a driver instance for testing
# Provides a driver instance to the tests
@pytest.fixture(scope="session")
def driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")  # Required for Docker
    options.add_argument("--disable-dev-shm-usage")  # Avoids issues with shared memory in Docker
    options.add_argument("--disable-gpu")  # Disable GPU in headless mode
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    yield driver
    driver.quit()
