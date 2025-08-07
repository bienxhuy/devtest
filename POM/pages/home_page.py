from POM.notifications.home_page_notifications import HomePageNotifications as Noti
from POM.pages.base_page import BasePage
from POM.locators.home_page_locators import HomePageLocators as el  

class HomePage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)

    # Header clicks 
    def click_home_header(self):
        return self.safe_click(
            el.HOME_HEADER,
            element="Home Header",
            success_message=Noti.HEADER_CLICKED_SUCCESS,
        )

    # Hero button clicks
    def click_start_learning(self):
        return self.safe_click(
            el.START_LEARNING_BUTTON,
            element="Start Learning button",
            success_message=Noti.START_BUTTON_CLICKED_SUCCESS,
        )
    
    # Click Enroll Course button
    def click_enroll_button(self):
        return self.safe_click(
            el.ENROLL_COURSE_BUTTON,
            element="Enroll Selenium Button",
            success_message=Noti.ENROLL_BUTTON_CLICKED_SUCCESS,
        )
