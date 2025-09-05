import pytest
from selenium import webdriver


# This is a pytest fixture that initializes a driver instance for testing
# Provides a driver instance to the tests
@pytest.fixture(scope="session")
def driver():
    options = webdriver.ChromeOptions()
    
    # Add required arguments for running Chrome in Docker
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    
    # Add these new options
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-browser-side-navigation")
    options.add_argument('--disable-infobars')
    
    # Specify a unique user data directory
    options.add_argument("--user-data-dir=/tmp/chrome-data")
    
    # Initialize Chrome driver with the options
    driver = webdriver.Chrome(options=options)
    
    # Set window size and position
    driver.set_window_size(1920, 1080)
    
    yield driver
    
    # Cleanup
    driver.quit()
