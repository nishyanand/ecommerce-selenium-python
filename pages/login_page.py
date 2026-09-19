"""
login_page.py
Page Object representing the TutorialsNinja Login Page.

Encapsulates:
- Locators for email, password, login button, and warning alerts
- Page action methods (enter credentials, submit, query login status)
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from utils.logger import get_logger

class LoginPage:
    """
    Page Object Model class for the Login Page.
    Separates DOM locators from test logic.
    """
    logger = get_logger(__name__)
    
    # -------------------------------------------------------------
    # 1. PAGE LOCATORS (Tuple of By and Locator string)
    # -------------------------------------------------------------
    EMAIL_INPUT = (By.ID, "input-email")
    PASSWORD_INPUT = (By.ID, "input-password")
    LOGIN_BUTTON = (By.CSS_SELECTOR, "input[value='Login']")
    WARNING_ALERT = (By.CSS_SELECTOR, "div.alert-danger")
    MY_ACCOUNT_HEADING = (By.XPATH, "//div[@id='content']//h2[text()='My Account']")

    def __init__(self, driver, timeout=10):
        """
        Initializes the LoginPage object with a WebDriver instance.
        """
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    # -------------------------------------------------------------
    # 2. NAVIGATION
    # -------------------------------------------------------------
    def open(self, base_url="https://tutorialsninja.com/demo/"):
        """Navigates directly to the login page."""
        login_url = f"{base_url.rstrip('/')}/index.php?route=account/login"
        self.driver.get(login_url)

    # -------------------------------------------------------------
    # 3. COMPONENT ACTIONS
    # -------------------------------------------------------------
    def enter_email(self, email):
        """Clears and types the email address into the email input field."""
        elem = self.wait.until(EC.visibility_of_element_located(self.EMAIL_INPUT))
        elem.clear()
        elem.send_keys(email)

    def enter_password(self, password):
        """Clears and types the password into the password input field."""
        elem = self.wait.until(EC.visibility_of_element_located(self.PASSWORD_INPUT))
        elem.clear()
        elem.send_keys(password)

    def click_login(self):
        """Clicks the Login submit button."""
        button = self.wait.until(EC.element_to_be_clickable(self.LOGIN_BUTTON))
        button.click()

    # -------------------------------------------------------------
    # 4. BUSINESS ACTION METHOD
    # -------------------------------------------------------------
    def login(self, email, password):
        """
        High-level business flow: enter email, enter password, and click login.
        """
        self.enter_email(email)
        self.enter_password(password)
        self.click_login()

    # -------------------------------------------------------------
    # 5. VERIFICATIONS & QUERIES
    # -------------------------------------------------------------
    def is_logged_in(self):
        """
        Returns True if the 'My Account' heading is visible after successful login,
        False otherwise.
        """
        try:
            heading = self.wait.until(EC.visibility_of_element_located(self.MY_ACCOUNT_HEADING))
            return heading.is_displayed()
        except TimeoutException:
            return False

    def get_error_message(self):
        """
        Retrieves the text of the warning alert banner when login fails.
        """
        try:
            alert = self.wait.until(EC.visibility_of_element_located(self.WARNING_ALERT))
            return alert.text.strip()
        except TimeoutException:
            return ""
