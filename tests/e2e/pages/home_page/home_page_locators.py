from selenium.webdriver.common.by import By


class HomePageLocators:
    # Navigation
    LOGIN_BUTTON = (By.XPATH, "//*[@id='home-action-button']")
    LOGOUT_BUTTON = LOGIN_BUTTON  # Same button, just different text
    QUOTE_PAGE_BUTTON = (By.XPATH, "//*[@id='home-quote-button']")

    # Hero text
    LOGGED_OUT_HERO = (By.XPATH, "//*[@id='home-greeting']")
    LOGGED_IN_HERO = LOGGED_OUT_HERO  # They're the same
    