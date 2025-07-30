from POM.pages.base_page import BasePage
from POM.locators.home_page_locators import HomePageLocators as el  

class HomePage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)

    # Header clicks 
    def click_home_header(self):
        self.safe_click(
            el.HOME_HEADER,
            description="Home Header",
            fallback_message=(
                "[click_home_header] Home header locator not found"
            )
        )

    def click_courses_header(self):
        self.safe_click(
            el.COURSES_HEADER,
            description="Courses Header",
            fallback_message=(
                "[click_courses_header] Courses header locator not found"
            )
        )

    def click_resources_header(self):
        self.safe_click(
            el.RESOURCES_HEADER,
            description="Resources Header",
            fallback_message=(
                "[click_resources_header] Resources header locator not found"
            )
        )

    def click_community_header(self):
        self.safe_click(
            el.COMMUNITY_HEADER,
            description="Community Header",
            fallback_message=(
                "[click_community_header] Community header locator not found"
            )
        )

    def click_about_header(self):
        self.safe_click(
            el.ABOUT_HEADER,
            description="About Header",
            fallback_message=(
                "[click_about_header] About header locator not found"
            )
        )

    def click_contact_header(self):
        self.safe_click(
            el.CONTACT_HEADER,
            description="Contact Header",
            fallback_message=(
                "[click_contact_header] Contact header locator not found"
            )
        )

    # Hero button clicks
    def click_start_learning(self):
        self.safe_click(
            el.START_LEARNING_BUTTON,
            description="Start Learning button"
        )

    def click_watch_demo(self):
        self.safe_click(
            el.WATCH_DEMO_BUTTON,
            description="Watch Demo button"
        )
    
    # Click Enroll Course buttons
    def click_all_enroll_button(self):
        buttons = self.driver.get_elements(el.ENROLL_COURSE_BUTTON)

        for index, button in enumerate(buttons, start=1):
            self.safe_click_element(
                button,
                description=f"Enroll Button #{index}"
            )      

    # Resource clicks       
    def click_pdf_resource_block(self):
        self.safe_click(
            el.RESOURCES_BLOCK_PDF,
            description="PDF resource block",
            fallback_message="[click_pdf_resource_block] Locator not found"
        )

    def click_video_resource_block(self):
        self.safe_click(
            el.RESOURCES_BLOCK_VIDEO,
            description="VIDEO resource block",
            fallback_message="[click_video_resource_block] Locator not found"
        )

    def click_codeex_resource_block(self):
        self.safe_click(
            el.RESOURCES_BLOCK_CODEEX,
            description="CODEEX resource block",
            fallback_message="[click_codeex_resource_block] Locator not found"
        )
        
    def click_resource_download_icon(self):
        self.safe_click(
            el.RESOURCES_DOWNLOAD_ICON,
            description="Resource Download Icon"
        )
