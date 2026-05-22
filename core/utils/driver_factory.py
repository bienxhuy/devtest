import os

from dotenv import load_dotenv
from selenium import webdriver


load_dotenv()


class DriverFactory:
    """Factory for creating Selenium WebDriver instances."""

    @staticmethod
    def create_driver():
        browser = os.getenv("BROWSER", "headless").strip().lower()
        if browser in {"chrome", "headless", "chrome-headless"}:
            options = webdriver.ChromeOptions()
            if browser != "chrome":
                options.add_argument("--headless")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-gpu")
            driver = webdriver.Chrome(options=options)
            driver.maximize_window()
            return driver

        raise ValueError(
            f"Unsupported BROWSER value: {browser}. "
            "Supported values are chrome, headless, and chrome-headless."
        )