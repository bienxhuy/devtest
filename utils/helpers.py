from datetime import datetime
from dotenv import load_dotenv
import os


# Create a directory for screenshots if it doesn't exist
# This is used to store screenshots taken a test session
load_dotenv()
BASE_SCREENSHOT_DIR = os.getenv('SCREENSHOT_DIR', 'utils/screenshots')
SCREENSHOT_DIR = os.path.join(
    BASE_SCREENSHOT_DIR, 
    os.getenv('SESSION_ID', 'none_specified_session'))
os.makedirs(SCREENSHOT_DIR, exist_ok=True)


def take_screenshot(driver, name="error"):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{name.replace(' ', '_')}_{timestamp}.png"
    filepath = os.path.join(SCREENSHOT_DIR, filename)
    
    try:
        driver.save_screenshot(filepath)
        return filepath
    except Exception as e:
        return f"Failed to take screenshot: {e}"
