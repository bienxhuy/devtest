from selenium.webdriver.common.by import By


class LoginPageLocators:
    LOGIN_EMAIL_INPUT = (By.XPATH, "//*[@id='login-email-input']")
    LOGIN_PASSWORD_INPUT = (By.XPATH, "//*[@id='login-password-input']")
    LOGIN_BUTTON = (By.XPATH, "//*[@id='login-submit-button']")

    REGISTER_NAME_INPUT = (By.XPATH, "//*[@id='register-name-input']")
    REGISTER_EMAIL_INPUT = (By.XPATH, "//*[@id='register-email-input']")
    REGISTER_PASSWORD_INPUT = (By.XPATH, "//*[@id='register-password-input']")
    REGISTER_BUTTON = (By.XPATH, "//*[@id='register-submit-button']")

    SWITCH_LOGIN_REGISTER_BUTTON = (By.XPATH, "//*[@id='auth-switch-mode-button']")
    BACK_TO_HOME_BUTTON = (By.XPATH, "//*[@id='login-back-home-button']")

    LOGIN_ERROR_MESSAGE = (By.XPATH, "//*[@id='login-error-message']")
    REGISTER_ERROR_MESSAGE = (By.XPATH, "//*[@id='register-error-message']")
    