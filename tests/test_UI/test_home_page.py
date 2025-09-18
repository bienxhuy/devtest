"""_summary_
This module contains tests for the HomePage class.
"""
import os
import pytest
from dotenv import load_dotenv
from POM.notifications.home_page_notifications import HomePageNotifications as Noti
from POM.pages.home_page import HomePage
from utils.helpers import take_screenshot


# Load environment variables from .env file
load_dotenv()
# Get the base URL from environment variables
BASE_URL = os.getenv('BASE_URL')


# This function tests the home page header click functionality
@pytest.mark.smoke
def test_click_header(driver):    
    # Initialize the HomePage object & navigate to the base URL
    page = HomePage(driver=driver)
    print(BASE_URL)
    driver.get(BASE_URL)
    
    try:
        # Click the home header and check the notification
        result = page.click_home_header()
        assert result == Noti.HEADER_CLICKED_SUCCESS, result
    except AssertionError as e:
        take_screenshot(driver, "header_click_error")
        raise e


# This function tests the Start Learning button click functionality
@pytest.mark.smoke
def test_click_start_button(driver):
    # Initialize the HomePage object & navigate to the base URL
    page = HomePage(driver=driver)
    driver.get(BASE_URL)
    
    try:
        # Click the Start Learning button and check the notification
        result = page.click_start_learning()
        assert result == Noti.START_BUTTON_CLICKED_SUCCESS, result
    except AssertionError as e:
        take_screenshot(driver, "start_button_click_error")
        raise e


# This function tests the Enroll Course button click functionality
@pytest.mark.smoke
def test_click_enroll_button(driver):
    # Initialize the HomePage object & navigate to the base URL
    page = HomePage(driver=driver)
    driver.get(BASE_URL)
    
    try:
        # Click the Enroll Course button and check the notification
        result = page.click_enroll_button()
        assert result == Noti.ENROLL_BUTTON_CLICKED_SUCCESS, result
    except AssertionError as e:
        take_screenshot(driver, "enroll_button_click_error")
        raise e

def test_env():
    """Test to ensure that the BASE_URL environment variable is set."""
    assert BASE_URL is not None, "BASE_URL environment variable is not set."