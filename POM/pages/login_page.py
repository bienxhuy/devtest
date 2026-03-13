from POM.locators.home_page_locators import HomePageLocators as el
from POM.pages.base_page import BasePage

class LoginPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
    
    def login(self, email, password):
        self.send_keys(el.LOGIN_EMAIL_INPUT, email, "Login Email Input")
        self.send_keys(el.LOGIN_PASSWORD_INPUT, password, "Login Password Input")
        return self.safe_click(el.LOGIN_BUTTON, "Clicked Login Button", "Login Button")
    
    def register(self, name, email, password):
        self.send_keys(el.REGISTER_NAME_INPUT, name, "Register Name Input")
        self.send_keys(el.REGISTER_EMAIL_INPUT, email, "Register Email Input")
        self.send_keys(el.REGISTER_PASSWORD_INPUT, password, "Register Password Input")
        return self.safe_click(el.REGISTER_BUTTON, "Clicked Register Button", "Register Button")
