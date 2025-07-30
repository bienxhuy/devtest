from POM.notifications.home_page_notifications import HomePageNotifications
from POM.pages.base_page import BasePage
from POM.locators.home_page_locators import HomePageLocators as el  

class HomePage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)

    # Header clicks 
    def click_home_header(self):
        isSuccess = self.safe_click(
            el.HOME_HEADER,
            description="Home Header",
            fallback_message=(
                "[click_home_header] Home header locator not found"
            )
        )
        if (isSuccess):
            return HomePageNotifications.HEADER_CLICKED_SUCCESS_NOTIFICATION

    # Hero button clicks
    def click_start_learning(self):
        isSuccess = self.safe_click(
            el.START_LEARNING_BUTTON,
            description="Start Learning button",
            fallback_message=(
                "[click_start_learning] Start Learning button locator not found"
            )
        )
        if (isSuccess):
            return HomePageNotifications.START_LEARNING_BUTTON_CLICKED_SUCCESS_NOTIFICATION
    
    # Click Enroll Course button
    def click_enroll_button(self):
        isSuccess = self.safe_click(
            el.ENROLL_COURSE_BUTTON,
            description="Enroll Selenium Button",
            fallback_message=(
                "[click_all_enroll_button] Enroll Selenium Button locator not found"
            )
        )
        if (isSuccess):
            return HomePageNotifications.ENROLL_COURSE_BUTTON_CLICKED_SUCCESS_NOTIFICATION
