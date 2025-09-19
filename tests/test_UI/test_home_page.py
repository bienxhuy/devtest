"""_summary_
This module contains tests for the HomePage class.
"""
import os
import pytest
from dotenv import load_dotenv
from POM.notifications.home_page_notifications import HomePageNotifications as Noti
from selenium.common.exceptions import WebDriverException
from POM.pages.home_page import HomePage
from utils.helpers import take_screenshot
from logs.logger import get_logger


# Load environment variables from .env file
load_dotenv()
# Get the base URL from environment variables
BASE_URL = os.getenv('BASE_URL')
# Get a logger instance for logging within the tests
logger = get_logger()


# This function tests the home page header click functionality
@pytest.mark.smoke
def test_click_header(driver):    
    logger.info(f"[TEST] - Start test: test_click_header with BASE_URL={BASE_URL}")
    logger.info(f"[TEST] - Initializing HomePage object.")
    page = HomePage(driver=driver)
    
    try:
        driver.get(BASE_URL)
    except WebDriverException as e:
        logger.error(f"[TEST] - Error navigating to {BASE_URL}: {e.msg}")
        raise RuntimeError(f"Error while navigating to {BASE_URL}") from e
    
    logger.info(f"[TEST] - Navigated to {BASE_URL}.")
    
    try:
        logger.info(f"[TEST] - Clicking the home header.")
        result = page.click_home_header()
        logger.info(f"[TEST] - Clicked the home header, received notification: {result}")
        assert result == Noti.HEADER_CLICKED_SUCCESS, result
    except AssertionError as e:
        logger.error(f"[TEST] - AssertionError in test_click_header: {e}")
        take_screenshot(driver, "header_click_error")
        raise


# This function tests the Start Learning button click functionality
@pytest.mark.smoke
def test_click_start_button(driver):
    logger.info(f"[TEST] - Start test: test_click_start_button with BASE_URL={BASE_URL}")
    logger.info(f"[TEST] - Initializing HomePage object.")
    page = HomePage(driver=driver)
    
    try:
        driver.get(BASE_URL)
    except WebDriverException as e:
        logger.error(f"[TEST] - Error navigating to {BASE_URL}: {e.msg}")
        raise RuntimeError(f"Error while navigating to {BASE_URL}") from e
    
    logger.info(f"[TEST] - Navigated to {BASE_URL}.")
    
    try:
        logger.info(f"[TEST] - Clicking the Start Learning button.")
        result = page.click_start_learning()
        logger.info(f"[TEST] - Clicked the Start Learning button, received notification: {result}")
        assert result == Noti.START_BUTTON_CLICKED_SUCCESS, result
    except AssertionError as e:
        logger.error(f"[TEST] - AssertionError in test_click_start_button: {e}")
        take_screenshot(driver, "start_button_click_error")
        raise


# This function tests the Enroll Course button click functionality
@pytest.mark.smoke
def test_click_enroll_button(driver):
    logger.info(f"[TEST] - Start test: test_click_enroll_button with BASE_URL={BASE_URL}")
    logger.info(f"[TEST] - Initializing HomePage object.")
    page = HomePage(driver=driver)
    
    try:
        driver.get(BASE_URL)
    except WebDriverException as e:
        logger.error(f"[TEST] - Error navigating to {BASE_URL}: {e.msg}")
        raise RuntimeError(f"Error while navigating to {BASE_URL}") from e
    
    logger.info(f"[TEST] - Navigated to {BASE_URL}.")
    
    try:
        logger.info(f"[TEST] - Clicking the Enroll Course button.")
        result = page.click_enroll_button()
        logger.info(f"[TEST] - Clicked the Enroll Course button, received notification: {result}")
        assert result == Noti.ENROLL_BUTTON_CLICKED_SUCCESS, result
    except AssertionError as e:
        logger.error(f"[TEST] - AssertionError in test_click_enroll_button: {e}")
        take_screenshot(driver, "enroll_button_click_error")
        raise
