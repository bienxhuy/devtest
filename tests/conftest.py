import pytest
from selenium import webdriver
from logs.logger import get_logger
from utils.helpers import take_screenshot


# Get a logger instance for logging within the tests
logger = get_logger()


# This is a pytest fixture that initializes a driver instance for testing
# Provides a driver instance to the tests
@pytest.fixture(scope="session")
def driver():
    logger.info("[CONFTEST] - Initialize WebDriver instance for the test session.")
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")  # Required for Docker
    options.add_argument("--disable-dev-shm-usage")  # Avoids issues with shared memory in Docker
    options.add_argument("--disable-gpu")  # Disable GPU in headless mode
    driver = webdriver.Chrome(options=options)
    # driver.maximize_window()
    yield driver
    logger.info("[CONFTEST] - Quitting WebDriver instance after the test session.")
    driver.quit()
    

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # execute all other hooks to obtain the report object
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)
    

@pytest.fixture(autouse=True)
def screenshot_on_fail(request, driver):
    yield
    if hasattr(request.node, "rep_call") and request.node.rep_call.failed:
        take_screenshot(driver, f"{request.node.name}_error")