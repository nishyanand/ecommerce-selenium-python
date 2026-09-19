"""
product_page.py
Page Object representing the Product Details Page on TutorialsNinja.

Encapsulates:
- Locators for product title, quantity input, add to cart button, and AJAX success alert
- Actions: get_product_title, set_quantity, click_add_to_cart, go_to_cart_via_alert
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

class ProductPage:
    """
    Page Object Model class for Product Details.
    """

    # -------------------------------------------------------------
    # 1. PAGE LOCATORS
    # -------------------------------------------------------------
    PRODUCT_TITLE = (By.CSS_SELECTOR, "#content h1")
    QUANTITY_INPUT = (By.ID, "input-quantity")
    ADD_TO_CART_BUTTON = (By.ID, "button-cart")
    SUCCESS_ALERT = (By.CSS_SELECTOR, "div.alert-success")
    CART_LINK_IN_ALERT = (By.XPATH, "//div[contains(@class, 'alert-success')]//a[text()='shopping cart']")
    HEADER_CART_LINK = (By.XPATH, "//a[@title='Shopping Cart']")

    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    # -------------------------------------------------------------
    # 2. PAGE QUERIES
    # -------------------------------------------------------------
    def get_product_title(self):
        """Retrieves the main heading text of the displayed product."""
        elem = self.wait.until(EC.visibility_of_element_located(self.PRODUCT_TITLE))
        return elem.text.strip()

    # -------------------------------------------------------------
    # 3. ACTIONS
    # -------------------------------------------------------------
    def set_quantity(self, quantity):
        """Sets the quantity in the product details input box."""
        qty_box = self.wait.until(EC.visibility_of_element_located(self.QUANTITY_INPUT))
        qty_box.clear()
        qty_box.send_keys(str(quantity))

    def click_add_to_cart(self):
        """Clicks the Add to Cart button."""
        btn = self.wait.until(EC.element_to_be_clickable(self.ADD_TO_CART_BUTTON))
        btn.click()

    def get_success_message(self):
        """
        Waits for the asynchronous AJAX green success banner and returns its text.
        """
        alert = self.wait.until(EC.visibility_of_element_located(self.SUCCESS_ALERT))
        return alert.text.strip()

    def go_to_cart_via_alert(self):
        """
        Clicks the 'shopping cart' link directly inside the success alert banner.
        """
        # Ensure alert is visible first
        self.wait.until(EC.visibility_of_element_located(self.SUCCESS_ALERT))
        cart_link = self.wait.until(EC.element_to_be_clickable(self.CART_LINK_IN_ALERT))
        cart_link.click()

    def go_to_cart_via_header(self):
        """
        Clicks the 'Shopping Cart' link in the top navigation bar.
        """
        link = self.wait.until(EC.element_to_be_clickable(self.HEADER_CART_LINK))
        link.click()
