from datetime import datetime
from dotenv import load_dotenv
import os
from core.utils.logs import get_logger


# Create a directory for screenshots if it doesn't exist
# This is used to store screenshots taken during a test session
load_dotenv()

BASE_SCREENSHOT_DIR = os.getenv('SCREENSHOT_DIR', 'reports/screenshots')
SCREENSHOT_DIR = os.path.join(
    BASE_SCREENSHOT_DIR, 
    os.getenv('BUILD_NUMBER', 'none_specified_session'))
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

# Get a logger instance for logging within the helpers
logger = get_logger()


def take_screenshot(driver, name="error"):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{name.replace(' ', '_')}_{timestamp}.png"
    filepath = os.path.join(SCREENSHOT_DIR, filename)
    
    try:
        driver.save_screenshot(filepath)
        logger.info(f"[SCREENSHOT] - Screenshot saved to {filepath} for {name}")
        return filepath
    except Exception as e:
        logger.error(f"[SCREENSHOT] - Failed to take screenshot: {e}")
        return f"Failed to take screenshot for {name}"
