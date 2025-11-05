"""_summary_
This module contains tests for the HomePage class.
"""
import os
import pytest
from dotenv import load_dotenv
from POM.notifications.home_page_notifications import HomePageNotifications as Noti
from selenium.common.exceptions import WebDriverException
from POM.pages.home_page import HomePage
from logs.logger import get_logger


# Load environment variables from .env file
load_dotenv()
# Get the base URL from environment variables
BASE_URL = os.getenv('BASE_URL')
# Get a logger instance for logging within the tests
logger = get_logger()


@pytest.fixture
def navigate_home(driver):
    """Navigate to BASE_URL safely, return HomePage instance."""
    logger.info("[FIXTURE] Navigating to BASE_URL=%s", BASE_URL)
    try:
        driver.get(BASE_URL)
    except WebDriverException as e:
        logger.error("Error navigating to %s: %s", BASE_URL, e.msg)
        raise RuntimeError(f"Error while navigating to {BASE_URL}") from e

    logger.info("[FIXTURE] Navigation successful.")
    return HomePage(driver=driver)


@pytest.mark.smoke
def test_click_header(navigate_home):
    logger.info("[TEST] test_click_header starts")
    result = navigate_home.click_home_header()
    assert result == Noti.HEADER_CLICKED_SUCCESS
    logger.info("[TEST] Header click successful.")


@pytest.mark.smoke
def test_click_start_button(navigate_home):
    logger.info("[TEST] test_click_start_button starts")
    result = navigate_home.click_start_learning()
    assert result == Noti.START_BUTTON_CLICKED_SUCCESS
    logger.info("[TEST] Start button click successful.")


@pytest.mark.smoke
def test_click_enroll_button(navigate_home):
    logger.info("[TEST] test_click_enroll_button starts")
    result = navigate_home.click_enroll_button()
    assert result == Noti.ENROLL_BUTTON_CLICKED_SUCCESS
    logger.info("[TEST] Enroll button click successful.")

def test_fail_expected():
    assert False, "This test is designed to fail."
    
def test_success_one():
    assert True
    
def test_success_two():
    assert 1 + 1 == 2

def test_success_three():
    assert "hello".upper() == "HELLO"
