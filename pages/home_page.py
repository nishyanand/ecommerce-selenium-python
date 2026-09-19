"""
home_page.py
Page Object representing the TutorialsNinja Home & Search Results Page.

Encapsulates:
- Header search input and search button locators
- Search results grid locators
- Actions: search_product, get_product_results_count, is_product_in_results, select_product
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from utils.logger import get_logger

class HomePage:
    """
    Page Object Model class for the Home and Search Results page.
    """

    # -------------------------------------------------------------
    # 1. PAGE LOCATORS
    # -------------------------------------------------------------
    SEARCH_INPUT = (By.NAME, "search")
    SEARCH_BUTTON = (By.CSS_SELECTOR, "div#search button.btn")
    PRODUCT_CARDS = (By.CSS_SELECTOR, ".product-layout")
    SEARCH_HEADING = (By.CSS_SELECTOR, "#content h1")
    NO_PRODUCT_MESSAGE = (By.XPATH, "//p[contains(text(), 'There is no product that matches the search criteria.')]")

    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    # -------------------------------------------------------------
    # 2. NAVIGATION
    # -------------------------------------------------------------
    def open(self, base_url="https://tutorialsninja.com/demo/"):
        """Navigates to the application Home Page, dismisses any cookie banner, and ensures the search box is ready."""
        self.driver.get(base_url)
        # Dismiss cookie consent if present
        from utils.cookie_handler import dismiss_cookie_banner
        dismiss_cookie_banner(self.driver)
        # Wait for the search input to be visible before proceeding
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.SEARCH_INPUT))

    # -------------------------------------------------------------
    # 3. SEARCH ACTIONS
    # -------------------------------------------------------------
    def enter_search_query(self, query):
        """Clears and types the search query into the search input."""
        box = self.wait.until(EC.visibility_of_element_located(self.SEARCH_INPUT))
        box.clear()
        box.send_keys(query)

    def click_search(self):
        """Clicks the search icon button."""
        btn = self.wait.until(EC.element_to_be_clickable(self.SEARCH_BUTTON))
        btn.click()

    def search_product(self, product_name):
        """
        High-level business action: types product name and executes search.
        """
        self.enter_search_query(product_name)
        self.click_search()

    # -------------------------------------------------------------
    # 4. RESULTS QUERIES & NAVIGATION
    # -------------------------------------------------------------
    def get_search_results_count(self):
        """
        Returns the number of product cards displayed in the search results.
        """
        try:
            # Wait for search heading to appear
            self.wait.until(EC.visibility_of_element_located(self.SEARCH_HEADING))
            cards = self.driver.find_elements(*self.PRODUCT_CARDS)
            return len(cards)
        except TimeoutException:
            return 0

    def is_product_in_results(self, product_name):
        """
        Checks whether a product with the given title exists in the search results.
        """
        try:
            # Look for an <a> tag matching the exact product title
            locator = (By.LINK_TEXT, product_name)
            elem = self.wait.until(EC.visibility_of_element_located(locator))
            return elem.is_displayed()
        except TimeoutException:
            return False

    def select_product(self, product_name):
        """
        Clicks on the product title link from the results to open its details page.
        """
        locator = (By.LINK_TEXT, product_name)
        link = self.wait.until(EC.element_to_be_clickable(locator))
        link.click()

    def has_no_product_message(self):
        """
        Returns True if the 'no product matches' message is displayed.
        """
        try:
            msg = self.wait.until(EC.visibility_of_element_located(self.NO_PRODUCT_MESSAGE))
            return msg.is_displayed()
        except TimeoutException:
            return False
