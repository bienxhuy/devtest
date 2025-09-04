# """_summary_
# This module contains tests for the HomePage class.
# """
# import os
# import pytest
# import logging
# import time
# from dotenv import load_dotenv
# from POM.notifications.home_page_notifications import HomePageNotifications as Noti
# from POM.pages.home_page import HomePage
# from logs.logger import log_test_result
# from models.test_result.Field import Field
# from models.test_result.Status import Status
# from utils.helpers import take_screenshot


# # Load environment variables from .env file
# load_dotenv()
# # Get the base URL from environment variables
# BASE_URL = os.getenv('BASE_URL')


# # This function tests the home page header click functionality
# @pytest.mark.smoke
# def test_click_header(driver):
#     # Start time for the test
#     start_time = time.perf_counter()
    
#     # Initialize the Field object to store test results
#     testField = Field()
#     # Initialize the HomePage object & navigate to the base URL
#     page = HomePage(driver=driver)
#     driver.get(BASE_URL)
    
#     try:
#         # Click the home header and check the notification
#         result = page.click_home_header()
#         assert result == Noti.HEADER_CLICKED_SUCCESS, result
#         # Initialize the test result field
#         testField.set_status(Status.SUCCESS) \
#             .set_log_level(logging.INFO) \
#             .set_message(result)

#     except AssertionError as e:
#         take_screenshot(driver, "header_click_error")
#         # Initialize the test result field with failure status
#         testField.set_status(Status.FAILURE) \
#             .set_log_level(logging.ERROR) \
#             .set_message(str(e))
#         raise
    
#     finally:
#         end_time = time.perf_counter()
#         duration = end_time - start_time
#         # Set the duration of the test
#         testField.set_duration(duration)
#         # Log the test result
#         # log_test_result(testField)


# # This function tests the Start Learning button click functionality
# @pytest.mark.smoke
# def test_click_start_button(driver):
#     # Start time for the test
#     start_time = time.perf_counter()
    
#     # Initialize the Field object to store test results
#     testField = Field()
#     # Initialize the HomePage object & navigate to the base URL
#     page = HomePage(driver=driver)
#     driver.get(BASE_URL)
    
#     try:
#         # Click the Start Learning button and check the notification
#         result = page.click_start_learning()
#         assert result == Noti.START_BUTTON_CLICKED_SUCCESS, result
#         # Initialize the test result field
#         testField.set_status(Status.SUCCESS) \
#             .set_log_level(logging.INFO) \
#             .set_message(result)

#     except AssertionError as e:
#         take_screenshot(driver, "start_button_click_error")
#         # Initialize the test result field with failure status
#         testField.set_status(Status.FAILURE) \
#             .set_log_level(logging.ERROR) \
#             .set_message(str(e))
#         raise
    
#     finally:
#         end_time = time.perf_counter()
#         duration = end_time - start_time
#         # Set the duration of the test
#         testField.set_duration(duration)
#         # Log the test result
#         # log_test_result(testField)


# # This function tests the Enroll Course button click functionality
# @pytest.mark.smoke
# def test_click_enroll_button(driver):
#     # Start time for the test
#     start_time = time.perf_counter()
    
#     # Initialize the Field object to store test results
#     testField = Field()
#     # Initialize the HomePage object & navigate to the base URL
#     page = HomePage(driver=driver)
#     driver.get(BASE_URL)
    
#     try:
#         # Click the Enroll Course button and check the notification
#         result = page.click_enroll_button()
#         assert result == Noti.ENROLL_BUTTON_CLICKED_SUCCESS, result
#         # Initialize the test result field
#         testField.set_status(Status.SUCCESS) \
#             .set_log_level(logging.INFO) \
#             .set_message(result)

#     except AssertionError as e:
#         take_screenshot(driver, "enroll_button_click_error")
#         # Initialize the test result field with failure status
#         testField.set_status(Status.FAILURE) \
#             .set_log_level(logging.ERROR) \
#             .set_message(str(e))
#         raise
    
#     finally:
#         end_time = time.perf_counter()
#         duration = end_time - start_time
#         # Set the duration of the test
#         testField.set_duration(duration)
#         # Log the test result
#         # log_test_result(testField)

import time


def test_equal_pass():
    assert 10 == 10
    
    
def test_equal_fail():
    assert 10 == 5, "This is expected to be failed!"    


def test_string_pass():
    assert "hello" in "hello world"

    
def test_string_fail():
    assert "bye" in "hello world", "This is expected to be failed!"


def test_flaky():
    assert time.time() % 2 < 1, "This is expected to be failed sometimes!"