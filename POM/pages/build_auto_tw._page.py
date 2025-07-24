from POM.pages.base_page import BasePage
from POM.locators.build_auto_locators import BuildAutoLocators as el  

class PrimaryPage(BasePage):
    def __init__(self, browser):
        super().__init__(browser)
        self.browser = browser

    # Header clicks
    def click_header(self, header_name):
        locator_name = f"{header_name.upper()}_HEADER"
        locator = getattr(el, locator_name, None)
        if locator:
            element = self.get_element(locator)
            if element:
                element.click()
            else:
                print(f"Failed to click on the {header_name} header. Element not found.")
        else:
            print(f"Invalid header name: {header_name}")

    # Hero button clicks
    def click_start_learning(self):
        element = self.get_element(el.START_LEARNING_BUTTON)
        if element:
            element.click()
        else:
            print("Failed to click on 'Start Learning' button. Element not found.")

    def click_watch_demo(self):
        element = self.get_element(el.WATCH_DEMO_BUTTON)
        if element:
            element.click()
        else:
            print("Failed to click on 'Watch Demo' button. Element not found.")
    
    # Course enrollment button clicks
    def click_enroll_course_button(self, button_number):
        locator = getattr(el, f"ENROLL_COURSE_BUTTON{button_number}")
        element = self.get_element(locator)
        if element:
            element.click()
        else:
            print(f"Failed to click on the enroll course button {button_number}. Element not found.")
    
    # Resource clicks
    def click_resource_block(self, block_type):
        block_type = block_type.upper()
        locator_map = {
            "PDF": el.RESOURCES_BLOCK_PDF,
            "VIDEO": el.RESOURCES_BLOCK_VIDEO,
            "CODEEX": el.RESOURCES_BLOCK_CODEEX
        }
        locator = locator_map.get(block_type)
        if locator:
            element = self.get_element(locator)
            if element:
                element.click()
            else:
                print(f"Failed to click on {block_type} resource block. Element not found.")
        else:
            print(f"Invalid resource block type: {block_type}")

    def click_resource_download_icon(self):
        element = self.get_element(el.RESOURCES_DOWNLOAD_ICON)
        if element:
            element.click()
        else:
            print("Failed to click on download icon. Element not found.")
