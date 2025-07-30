import os
import pytest
from dotenv import load_dotenv
from POM.pages.home_page import HomePage
from logs.logger import get_logger


# Initialize the logger
logger = get_logger(__name__)


# Load environment variables from .env file
load_dotenv()
# Get the base URL from environment variables
BASE_URL = os.getenv('BASE_URL')


# This is a test for the home page of the application
# This test will ensure that the home page loads correctly,
# and all components are clickable
@pytest.mark.smoke
def test_all_components(driver):
    # Initialize the HomePage object
    page = HomePage(driver=driver)
    # Navigate to the base URL
    driver.get(BASE_URL)

    try:
        # Click on every component in the home page
        page.click_home_header()
        page.click_about_header()
        page.click_contact_header()
        page.click_courses_header()
        page.click_community_header()
        page.click_resources_header()
        page.click_start_learning()
        page.click_watch_demo()
        page.click_all_enroll_button()
        page.click_pdf_resource_block()
        page.click_video_resource_block()
        page.click_codeex_resource_block()
        page.click_resource_download_icon()

    except Exception as e:
        logger.error(f"An error occurred while clicking components: {e}")
