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
        
        self.safe_click(
        locator,
        description=f"{header_name} header",
        fallback_message=f"[click_header] Invalid header name: {header_name}")

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
    def click_resource_block(self, block_type):     
        block_type = block_type.upper()
        locator_map = {
            "PDF": el.RESOURCES_BLOCK_PDF,
            "VIDEO": el.RESOURCES_BLOCK_VIDEO,
            "CODEEX": el.RESOURCES_BLOCK_CODEEX
        }
        locator = locator_map.get(block_type)   

        self.safe_click(
                locator,
                description=f"{block_type} resource block",
                fallback_message=f"[click_resource_block] Invalid resource block type: {block_type}"
            )

    def click_resource_download_icon(self):
        self.safe_click(
            el.RESOURCES_DOWNLOAD_ICON,
            description="Resource Download Icon"
        )
