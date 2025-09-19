"""_summary_
This module contains tests for the HomePage class.
"""
import os
import pytest
from dotenv import load_dotenv
from POM.notifications.home_page_notifications import HomePageNotifications as Noti
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
    # Initialize the HomePage object & navigate to the base URL
    logger.info(f"Start test: test_click_header with BASE_URL={BASE_URL}")
    logger.info(f"Initializing HomePage object.")
    page = HomePage(driver=driver)
    try:
        driver.get(BASE_URL)
    except AssertionError as e:
        logger.error(f"Error navigating to {BASE_URL}")
        raise f"Error while navigating to {BASE_URL}"
    logger.info(f"Navigated to {BASE_URL}.")
    
    try:
        # Click the home header and check the notification
        logger.info(f"Clicking the home header.")
        result = page.click_home_header()
        logger.info(f"Clicked the home header, received notification: {result}")
        assert result == Noti.HEADER_CLICKED_SUCCESS, result
    except AssertionError as e:
        logger.error(f"AssertionError in test_click_header: {e}")
        take_screenshot(driver, "header_click_error")
        raise "Error in test_click_header"


# This function tests the Start Learning button click functionality
@pytest.mark.smoke
def test_click_start_button(driver):
    # Initialize the HomePage object & navigate to the base URL
    logger.info(f"Start test: test_click_start_button with BASE_URL={BASE_URL}")
    logger.info(f"Initializing HomePage object.")
    page = HomePage(driver=driver)
    try:
        driver.get(BASE_URL)
    except AssertionError as e:
        logger.error(f"Error navigating to {BASE_URL}")
        raise f"Error while navigating to {BASE_URL}"
    logger.info(f"Navigated to {BASE_URL}.")
    
    try:
        # Click the Start Learning button and check the notification
        logger.info(f"Clicking the Start Learning button.")
        result = page.click_start_learning()
        logger.info(f"Clicked the Start Learning button, received notification: {result}")
        assert result == Noti.START_BUTTON_CLICKED_SUCCESS, result
    except AssertionError as e:
        logger.error(f"AssertionError in test_click_start_button: {e}")
        take_screenshot(driver, "start_button_click_error")
        raise "Error in test_click_start_button"


# This function tests the Enroll Course button click functionality
@pytest.mark.smoke
def test_click_enroll_button(driver):
    # Initialize the HomePage object & navigate to the base URL
    logger.info(f"Start test: test_click_enroll_button with BASE_URL={BASE_URL}")
    logger.info(f"Initializing HomePage object.")
    page = HomePage(driver=driver)
    try:
        driver.get(BASE_URL)
    except AssertionError as e:
        logger.error(f"Error navigating to {BASE_URL}")
        raise f"Error while navigating to {BASE_URL}"
    logger.info(f"Navigated to {BASE_URL}.")
    
    try:
        # Click the Enroll Course button and check the notification
        logger.info(f"Clicking the Enroll Course button.")
        result = page.click_enroll_button()
        logger.info(f"Clicked the Enroll Course button, received notification: {result}")
        assert result == Noti.ENROLL_BUTTON_CLICKED_SUCCESS, result
    except AssertionError as e:
        logger.error(f"AssertionError in test_click_enroll_button: {e}")
        take_screenshot(driver, "enroll_button_click_error")
        raise "Error in test_click_enroll_button"
