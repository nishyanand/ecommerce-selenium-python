"""
screenshot_helper.py
Utility module for capturing screenshots during test execution and failures.
"""

from datetime import datetime
from pathlib import Path

SCREENSHOTS_DIR = Path(__file__).resolve().parent.parent / "screenshots"

def take_screenshot(driver, name):
    """
    Captures a full browser screenshot and saves it to the screenshots/ directory.
    
    Args:
        driver: Active Selenium WebDriver instance.
        name (str): Meaningful name for the screenshot (e.g. 'login_success').
        
    Returns:
        str: Absolute file path of the saved screenshot.
    """
    # Ensure directory exists
    SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)
    
    # Generate timestamped filename for uniqueness
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    clean_name = name.replace(" ", "_").replace("/", "_")
    filename = f"{clean_name}_{timestamp}.png"
    filepath = SCREENSHOTS_DIR / filename
    
    # Capture screenshot via Selenium API
    driver.save_screenshot(str(filepath))
    return str(filepath)
