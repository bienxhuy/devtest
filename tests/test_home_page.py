"""_summary_
This module contains tests for the HomePage class.
"""
import os
import pytest
from dotenv import load_dotenv
from POM.notifications.home_page_notifications import HomePageNotifications as Noti
from POM.pages.home_page import HomePage
from logs.logger import get_logger


# Initialize the logger
logger = get_logger(__name__)


# Load environment variables from .env file
load_dotenv()
# Get the base URL from environment variables
BASE_URL = os.getenv('BASE_URL')


# This function tests the home page header click functionality
@pytest.mark.smoke
def test_click_header(driver):
    # Initialize the HomePage object
    page = HomePage(driver=driver)
    # Navigate to the base URL
    driver.get(BASE_URL)
    # Click the home header and check the notification
    notification = page.click_home_header()
    assert notification == Noti.HEADER_CLICKED_SUCCESS_NOTIFICATION
        

# This function tests the Start Learning button click functionality
@pytest.mark.smoke
def test_click_start_learning_button(driver):
    # Initialize the HomePage object
    page = HomePage(driver=driver)
    # Navigate to the base URL
    driver.get(BASE_URL)
    # Click the Start Learning button and check the notification
    notification = page.click_start_learning()
    assert notification == Noti.START_LEARNING_BUTTON_CLICKED_SUCCESS_NOTIFICATION


# This function tests the Enroll Course button click functionality
@pytest.mark.smoke
def test_click_enroll_button(driver):
    # Initialize the HomePage object
    page = HomePage(driver=driver)
    # Navigate to the base URL
    driver.get(BASE_URL)
    # Click the Enroll Course button and check the notification
    notification = page.click_enroll_button()
    assert notification == Noti.ENROLL_COURSE_BUTTON_CLICKED_SUCCESS_NOTIFICATION
