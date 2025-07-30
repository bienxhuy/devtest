import os
import sys
import pytest
from dotenv import load_dotenv
from POM.pages.home_page import HomePage


# Load environment variables from .env file
load_dotenv()
# Get the base URL from environment variables
BASE_URL = os.getenv('BASE_URL')


# This is a test for the home page of the application
# This test will ensure that the home page loads correctly,
# and all components are clickable
@pytest.mark.smoke
def test_build_auto_tw_page(driver):
    # Initialize the HomePage object
    page = HomePage(driver=driver)
    # Navigate to the base URL
    driver.get(BASE_URL)

    # Click on every component in the page
    # TODO: Implement the logic to click on each component
    # Example:
    # page.click_resource_download_icon()
