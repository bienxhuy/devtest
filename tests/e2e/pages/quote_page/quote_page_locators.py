from selenium.webdriver.common.by import By


class QuotePageLocators:
    # Always visible
    REFRESH_BUTTON = (By.XPATH, "//*[@id='refresh-button']")
    FIRST_QUOTE_TEXT = (By.XPATH, "(//article[@role='button' and starts-with(@aria-label,'Open quote by')])[1]//p")

    # Authenticated only
    NEW_QUOTE_BUTTON = (By.XPATH, "//*[@id='new-quote-button']")

    # Create quote modal
    QUOTE_TEXT_INPUT = (By.XPATH, "//*[@id='quote-textarea']")
    POST_QUOTE_BUTTON = (By.XPATH, "//*[@id='quote-submit-button']")

    # Delete flow
    FIRST_OWN_QUOTE_DELETE_BUTTON = (By.XPATH, "((//article[@role='button' and starts-with(@aria-label,'Open quote by')][.//button[normalize-space()='Delete']])[1]//button[normalize-space()='Delete'])")
    CONFIRM_DELETE_BUTTON = (By.XPATH, "//div[@role='dialog' and @data-state='open']//button[normalize-space()='Delete']")
