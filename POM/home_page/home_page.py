from POM.home_page.home_page_notifications import HomePageNotifications as Noti
from POM.base_page import BasePage
from POM.home_page.home_page_locators import HomePageLocators as el


class HomePage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.go_to_url(self.BASE_URL)

    # Click home action button
    def click_home_action_button(self):
        self.click(el.HOME_ACTION_BUTTON)
        return Noti(self.driver)

    # Check home header
    def check_home_header(self, expected_header):
        actual_header = self.get_inner_text(el.HOME_HEADER)
        return actual_header == expected_header
