import os
import pytest
from dotenv import load_dotenv

from core.utils.driver_factory import DriverFactory
from core.utils.logs import get_logger
from core.utils.screenshot import take_screenshot


load_dotenv()
logger = get_logger()


@pytest.fixture(scope="session")
def base_url():
    return os.getenv("FE_URL")


@pytest.fixture(scope="function")
def driver():
    """Initialize and teardown a WebDriver per test."""
    logger.info("[CONFTEST] - Initialize WebDriver instance for the test session.")
    web_driver = DriverFactory.create_driver()
    yield web_driver
    logger.info("[CONFTEST] - Quitting WebDriver instance after the test session.")
    web_driver.quit()


# Fixtures for taking screenshots on failure
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # Execute all other hooks first to obtain the report object.
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)


@pytest.fixture(autouse=True)
def screenshot_on_fail(request, driver):
    """Capture screenshot when a test fails."""
    yield
    if hasattr(request.node, "rep_call") and request.node.rep_call.failed:
        take_screenshot(driver, f"{request.node.name}_error")